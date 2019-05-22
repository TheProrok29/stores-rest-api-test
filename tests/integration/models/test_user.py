from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', '1234')

            self.assertIsNone(UserModel.find_by_username('test'), 'Found user "test" before save_to_db')
            self.assertIsNone(UserModel.find_by_id(1), 'Found user with id 1 before save_to_db')

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('test'), 'Not found user "test" in db after save_to_db')
            self.assertIsNotNone(UserModel.find_by_id(1), 'Not found user with id 1 in db after save_to_db')

            user.delete_from_db()

            self.assertIsNone(UserModel.find_by_username('test'), 'Not deleted user after delete delete_from_db')
            self.assertIsNone(UserModel.find_by_id(1), 'Not deleted user after delete delete_from_db')