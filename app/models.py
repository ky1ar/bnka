from app import db

class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account = db.Column(db.Integer, nullable=False)
    inout = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, user_id, account, inout, amount):
        self.user_id = user_id
        self.account = account
        self.inout = inout
        self.amount = amount

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, default=1000.0)

    transactions = db.relationship(Transactions, backref='user', lazy=True)

    def __init__(self, dni, name, last, date, email, phone, amount=1000.0):
        self.dni = dni
        self.name = name
        self.last = last
        self.date = date
        self.email = email
        self.phone = phone
        self.amount = amount


        


