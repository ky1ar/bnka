from abc import ABC, abstractmethod
from app.models import Users, Transactions, db
from sqlalchemy.orm import joinedload
from sqlalchemy import func

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, dni, name, last, date, email, phone):
        pass

    @abstractmethod
    def update_user(self, user_id, dni, name, last, date, email, phone):
        pass
    
    @abstractmethod
    def search_user(self, dni):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def update_user_trans(self, user_id, amount):
        pass 

    @abstractmethod
    def search_user_trans(self, dni):
        pass     
    
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_full_user(self):
        pass

# Repositorio de Usuarios con Excepción de errores
class UserRepository(IUserRepository):
    def create_user(self, dni, name, last, date, email, phone):
        try:
            user = Users(dni=dni, name=name, last=last, date=date, email=email, phone=phone)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update_user(self, user_id, dni, name, last, date, email, phone):
        try:
            user = Users.query.get(user_id)
            if user:
                user.dni = dni
                user.name = name
                user.last = last
                user.date = date
                user.email = email
                user.phone = phone
                db.session.commit()
                return user
            return None
        except Exception as e:
            db.session.rollback()
            raise e
    
    def search_user(self, dni):
        return Users.query.filter_by(dni=dni).first()
    
    def delete_user(self, user_id):
        try:
            user = Users.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    def update_user_trans(self, user_id, amount):
        try:
            user = Users.query.get(user_id)
            if user:
                user.amount = amount
                db.session.commit()
                return user
            return None
        except Exception as e:
            db.session.rollback()
            raise e
        
    def search_user_trans(self, dni):
        user = Users.query.filter_by(dni=dni).options(joinedload(Users.transactions)).first()     
        if user:
            user_data = {
                **user.__dict__,
                "transactions": [{
                    "id": Users.query.get(transaction.account).dni,
                    "amount": transaction.amount,
                    "inout": transaction.inout,
                    "account": transaction.account,
                    "timestamp": transaction.timestamp
                } for transaction in user.transactions]
            }
            return user_data
        else:
            return None
    
    def get_all_users(self):
        return Users.query.all()

    def get_full_user(self):
        subquery = db.session.query(
            Transactions.user_id,
            func.max(Transactions.timestamp).label('latest_timestamp')
        ).group_by(Transactions.user_id).subquery()

        latest_amount_query = db.session.query(
            Transactions.user_id,
            Transactions.amount.label('latest_amount')
        ).join(
            subquery,
            db.and_(
                Transactions.user_id == subquery.c.user_id,
                Transactions.timestamp == subquery.c.latest_timestamp
            )
        )

        latest_amount_subquery = latest_amount_query.subquery()

        query = db.session.query(
            Users,
            latest_amount_subquery.c.latest_amount
        ).outerjoin(
            latest_amount_subquery,
            Users.id == latest_amount_subquery.c.user_id
        )

        users_with_latest_amount = query.all()
        return users_with_latest_amount


class ITransactionsRepository(ABC):
    @abstractmethod
    def create_trans(self, user_id, recipient_id, inout, amount):
        pass


class TransactionsRepository(ITransactionsRepository):
    def create_trans(self, user_id, recipient_id, inout, amount):
        try:
            transaction = Transactions(user_id=user_id, account=recipient_id, inout=inout, amount=amount)
            db.session.add(transaction)
            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            raise e