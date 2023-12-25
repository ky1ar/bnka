from app.repositories import UserRepository

class UserVerifier:
    @staticmethod
    def verify_user_exists(dni):
        user_repo = UserRepository()
        return user_repo.search_user(dni) is not None
    
    @staticmethod
    def verify_user_account(dni, account):
        return dni == account is not None
    
    @staticmethod
    def verify_amount(user_amount, amount):
        return user_amount > amount is not None