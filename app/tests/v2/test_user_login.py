import unittest
import os
import json
from app import create_app
from app.models.v2 import User


class LoginUserTestCase(unittest.TestCase):
    """This class implements Login user TestCases"""

    def setUp(self):
        """Will be called before every test"""
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

    def tearDown(self):
        """ clear data after every test"""
        User.query.delete()

    def test_user_can_login(self):
        """Test user can login to get access token"""
        # Create_user
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": "application/json"}
        )
        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.logins),
            headers={"content-type": "application/json"}
        )
        # self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token", str(login.data))

    def test_cannot_login_if_not_registered(self):
        """ Test that only registered users can login"""
        User.query.delete()  # clears users
        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.logins),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(login.status_code, 401)
        self.assertIn("Username not found!", str(login.data))

    def test_login_details_required(self):
        """Test that all login fields are required"""
        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps({
                "username": "",
                "password": ""
            }),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(login.status_code, 401)
        self.assertIn("Field cannot be empty", str(login.data))


if __name__ == "__main__":
    unittest.main()
