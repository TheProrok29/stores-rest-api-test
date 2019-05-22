from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_create_user(self):
        user = UserModel('test', '1234')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, '1234')