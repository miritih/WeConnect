import unittest
import os
import json
from app import create_app, user_model


class LoginUserTestCase(unittest.TestCase):
    """This class implements Login user TestCases"""

    def setUp(self):
        """Will be called before every test"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {"username": "miriti", "password": "123",
                     "first_name": "eric", "last_name": "Miriti"}
        self.logins = {"username": "miriti", "password": "123"}

    def tearDown(self):
        """ clear data after every test"""
        user_model.users.clear()

    def test_user_can_login(self):
        """Test user can login to get access token"""
        register = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                                      content_type='application/json')
        login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                   content_type='application/json')
        self.assertEqual(login.status_code, 200)

    def test_cannot_login_if_not_registered(self):
        """ Test that only registered users can login"""
        login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                   content_type='application/json')
        self.assertEqual(login.status_code, 401)
        assert b'{\n  "message": "Username not found!"\n}\n' in login.data

if __name__ == "__main__":
    unittest.main()
