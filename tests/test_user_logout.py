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
        data = json.loads(login.data.decode("utf-8"))
        token = data['auth_token']
        logout = self.client().post('/api/v1/auth/logout', data={},
                                    headers={"content_type": "application/json", "x-access-token": token})
        self.assertEqual(logout.status_code, 200)
