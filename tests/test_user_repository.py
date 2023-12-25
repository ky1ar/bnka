import unittest
from datetime import datetime
from app.models import Users
from app.repositories import UserRepository
from app import db, app

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'
        app.config['TESTING'] = True

        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

        user_1 = Users(dni='1234567890', name='John', last='Doe', date=datetime.now(), email='john@example.com', phone='1234567890')
        user_2 = Users(dni='0987654321', name='Jane', last='Smith', date=datetime.now(), email='jane@example.com', phone='9876543210')

        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

    def test_delete_user(self):

        user_id_to_delete = 1

        user_repo = UserRepository()
        result = user_repo.delete_user(user_id_to_delete)

        self.assertTrue(result)

        deleted_user = Users.query.get(user_id_to_delete)
        self.assertIsNone(deleted_user)

    def tearDown(self):

        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()
