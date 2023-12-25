from flask import render_template, request, redirect, url_for, jsonify, session, flash, get_flashed_messages
from app import app
from app.models import Users
from app.repositories import UserRepository, TransactionsRepository
from app.validators import Validator
from app.verifiers import UserVerifier
from datetime import datetime


@app.route('/')
def home_route():
    user_repo = UserRepository()

    return home(user_repo=user_repo)


@app.route('/create', methods=['POST'])
def create_route():
    user_repo = UserRepository()
    validator = Validator()
    user_verifier = UserVerifier()

    return create(user_repo=user_repo, validator=validator, user_verifier=user_verifier)


@app.route('/user', methods=['POST'])
def user_route():
    user_repo = UserRepository()
    user_verifier = UserVerifier()

    return user(user_repo=user_repo, user_verifier=user_verifier)


@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_route(user_id):
    user_repo = UserRepository()

    return delete(user_id, user_repo=user_repo)
    

@app.route('/update', methods=['POST'])
def update_route():
    user_repo = UserRepository()
    validator = Validator()

    return update(user_repo=user_repo, validator=validator)


@app.route('/trans', methods=['POST'])
def trans_route():
    user_repo = UserRepository()
    trans_repo = TransactionsRepository()
    validator = Validator()
    user_verifier = UserVerifier()

    return trans(user_repo=user_repo, trans_repo=trans_repo, validator=validator, user_verifier=user_verifier)


#Version para Estilos y JS
@app.context_processor
def inject_version():
    return {'version': app.config['VERSION']}

def home(user_repo=None):
    user_repo = user_repo or UserRepository()

    message = get_flashed_messages()
    users = user_repo.get_all_users()
    return render_template('index.html', users=users, message=message)


def create(user_repo=None, validator=None, user_verifier=None):
    user_repo = user_repo or UserRepository()
    validator = validator or Validator()
    user_verifier = user_verifier or UserVerifier()

    data = request.form.to_dict()
    dni = data['dni']
    name = data['name']
    last = data['last']
    date = data['date']
    email = data['email']
    phone = data['phone']
    
    if user_verifier.verify_user_exists(dni):
        return jsonify({"message": "Ya existe una cuenta asociada a este DNI"})

    if not all(data.values()):
        return jsonify({"message": "Todos los campos son obligatorios. Por favor, complete todos los campos."})

    if not validator.validate_dni(dni):
        return jsonify({"message": "El DNI debe contener solo números."})
    
    if not validator.validate_name_last(name, last):
        return jsonify({"message": "El nombre y el apellido no deben contener números o símbolos."})

    if not validator.validate_email(email):
        return jsonify({"message": "El formato de correo electrónico es inválido."})

    if not validator.validate_phone(phone):
        return jsonify({"message": "El número de teléfono debe contener solo números."})

    if user_repo.create_user(dni, name, last, datetime.strptime(date, '%Y-%m-%d').date(), email, phone):
        flash('Usuario creado exitosamente')
        return jsonify({"message": "OK"})
    else:
        session['message'] = 'Hubo un error'


def user(user_repo=None, user_verifier=None):
    user_repo = user_repo or UserRepository()
    user_verifier = user_verifier or UserVerifier()

    dni = request.form['dni'].strip()
    users = user_repo.get_all_users()

    if not dni:
        flash('Ingrese el número de DNI', 'warning')
        return redirect(url_for('home_route'))
    
    if user_verifier.verify_user_exists(dni):
        user = user_repo.search_user_trans(dni)
        return render_template('index.html', users=users, user=user)
    else:
        flash('No se encuentra cuenta relacionada a ese DNI', 'error')
        return redirect(url_for('home_route'))


def delete(user_id, user_repo=None):
    user_repo = user_repo or UserRepository()

    if user_repo.delete_user(user_id):
        flash('Usuario eliminado exitosamente', 'success')
        return redirect(url_for('home_route'))
    else:
        flash('No se encontró el usuario', 'error')


def update(user_repo=None, validator=None):
    user_repo = user_repo or UserRepository()
    validator = validator or Validator()

    data = request.form.to_dict()
    user_id = data['user_id']
    dni = data['dni']
    name = data['name']
    last = data['last']
    date = data['date']
    email = data['email']
    phone = data['phone']

    if not all(data.values()):
        return jsonify({"message": "Todos los campos son obligatorios. Por favor, complete todos los campos."})

    if not validator.validate_dni(dni):
        return jsonify({"message": "El DNI debe contener solo números."})
    
    if not validator.validate_name_last(name, last):
        return jsonify({"message": "El nombre y el apellido no deben contener números o símbolos."})

    if not validator.validate_email(email):
        return jsonify({"message": "El formato de correo electrónico es inválido."})

    if not validator.validate_phone(phone):
        return jsonify({"message": "El número de teléfono debe contener solo números."})

    if user_repo.update_user(user_id, dni, name, last, datetime.strptime(date, '%Y-%m-%d').date(), email, phone):
        flash('Usuario actualizado exitosamente')
        return jsonify({"message": "OK"})
    else:
        return "Usuario no encontrado"
    

def trans(user_repo=None, trans_repo=None, validator=None, user_verifier=None):
    user_repo = user_repo or UserRepository()
    trans_repo = trans_repo or TransactionsRepository()
    validator = validator or Validator()
    user_verifier = user_verifier or UserVerifier()

    data = request.form.to_dict()
    dni = data['dni']
    account = data['account']
    amount = data['amount']
    
    if not user_verifier.verify_user_exists(account):
        return jsonify({"message": "No existe una cuenta asociada a este DNI"})
    
    if user_verifier.verify_user_account(dni, account):
        return jsonify({"message": "No puedes transferir a tu propia cuenta."})
    
    if not all(data.values()):
        return jsonify({"message": "Todos los campos son obligatorios. Por favor, complete todos los campos."})
    
    if not validator.validate_phone(amount):
        return jsonify({"message": "Ingrese un monto válido."})
    
    user = user_repo.search_user(dni)
    recipient = user_repo.search_user(account)
    user_balance = user.amount - float(amount)
    recipient_balance = recipient.amount + float(amount)

    if not user_verifier.verify_amount(user.amount, float(amount)):
        return jsonify({"message": "No hay suficiente saldo en la cuenta."})
    
    user_trans = trans_repo.create_trans(user.id, recipient.id, 0, amount)
    recipient_trans = trans_repo.create_trans(recipient.id, user.id, 1, amount)
    update_user = user_repo.update_user_trans(user.id, user_balance)
    update_recipent = user_repo.update_user_trans(recipient.id, recipient_balance)

    if user_trans and recipient_trans and update_user and update_recipent:
        flash('Transacción exitosa')
        return jsonify({"message": "OK"})
    else:
        flash('Hubo un error')
        return jsonify({"message": "OK"}) 
