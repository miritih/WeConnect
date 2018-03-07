import unittest
import os
import json
from app import create_app, user_model


class LogoutUserTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {"username": "miriti", "password": "123",
                     "first_name": "eric", "last_name": "Miriti"}
        self.logins = {"username": "miriti", "password": "123"}

    def tearDown(self):
        """ clear data after every test"""
        user_model.users.clear()

    def test_user_can_logout(self):
        """Tests users can logout"""
        register = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                                      content_type='application/json')
        login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                   content_type='application/json')
        data = json.loads(login.get_data(as_text=True))
        token = data['auth_token']
        logout = self.client().post('/api/v1/auth/logout', data={},
                                    headers={"content_type": "application/json", "access-token": token})
        self.assertEqual(login.status_code, 200)

    def test_user_needs_token_to_logout(self):
        """test that you must be logged for you to logout"""
        res = self.client().post('/api/v1/auth/logout', data={},
                                 headers={"content_type": "application/json"})
        self.assertEqual(res.status_code, 401)
        assert b'{\n  "message": "Token is missing, login to get token"\n}\n' in res.data
