import unittest
import os
import json
from app import create_app, user_model


class ChangePasswordTestCase(unittest.TestCase):
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
        self.changepass = {'password': '1234'}

    def tearDown(self):
        """ clear data after every test"""
        user_model.users.clear()

    def test_can_change_password(self):
        """Tests users can logout"""
        self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                           content_type='application/json')

        login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                   content_type='application/json')
        data = json.loads(login.get_data(as_text=True))
        token = data['auth_token']
        reset = self.client().put('/api/v1/auth/reset-password', data=json.dumps(self.changepass),
                                  headers={"content-type": "application/json", "access-token": token})
        assert b'{\n  "message": "password updated"\n}\n' in reset.data
