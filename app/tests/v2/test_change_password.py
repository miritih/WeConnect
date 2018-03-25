import unittest
import os
import json
from app import create_app
from app.models.v2 import User


class ChangePasswordTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app('testing')
        self.app.app_context().push()
        self.client = self.app.test_client
        self.user = {
            "username": "mwenda",
            "email": "ericmwenda5@gmail.com",
            "password": "qwerty123!@#",
            "first_name": "eric",
            "last_name": "Miriti"
        }
        self.logins = {
            "username": "mwenda",
            "password": "qwerty123!@#"
        }
        self.changepass = {
            'password': '12345qwert',
            "old_password": "qwerty123!@#"
        }
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        self.login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.logins),
            content_type='application/json'
        )
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        User.query.delete()

    def test_can_change_password(self):
        """Tests users can update password"""

        reset = self.client().put(
            '/api/v2/auth/reset-password',
            data=json.dumps(self.changepass),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("password updated", str(reset.data))

    def test_password_required(self):
        """tests password must be given"""
        reset = self.client().put(
            '/api/v2/auth/reset-password',
            data=json.dumps({
                "password": "",
                "old_password": "qwtqwy"
            }),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("Password must be 6-20 Characters", str(reset.data))

    def test_password_validation(self):
        """Test password must be 6-20 characters, alphanumeric"""
        reset = self.client().put(
            '/api/v2/auth/reset-password',
            data=json.dumps({
                "password": "123", "old_password": "qwtqwy"
            }),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(reset.status_code, 401)
        self.assertIn(
            "Password must be 6-20 Characters and can only contains leters",
            str(reset.data)
        )

    def test_wrong_old_password(self):
        """Test old password is required to change password"""
        reset = self.client().put(
            '/api/v2/auth/reset-password',
            data=json.dumps({
                "password": "qwertyu123",
                "old_password": "qwtqwy"
            }),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(reset.status_code, 406)
        self.assertIn("Wrong old Password", str(reset.data))
