import unittest
import os
import json
from app import create_app
from app.v1 import business_model, user_model


class ChangePasswordTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {"username": "miriti", "password": "qwerty123!@#",
                     "first_name": "eric", "last_name": "Miriti"}
        self.logins = {"username": "miriti", "password": "qwerty123!@#"}
        self.changepass = {'password': 'qwerty123!@#%',
                           "old_password": "qwerty123!@#"}
        self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                           content_type='application/json')

        self.login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                        content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        user_model.users.clear()

    def test_can_change_password(self):
        """Tests users can update password"""

        reset = self.client().put('/api/v1/auth/reset-password', data=json.dumps(self.changepass),
                                  headers={"content-type": "application/json", "access-token": self.token})
        assert b'{\n  "message": "password updated"\n}\n' in reset.data

    def test_password_required(self):
        """tests password must be given"""
        reset = self.client().put('/api/v1/auth/reset-password',
                                  data=json.dumps(
                                      {"password": "", "old_password": "qwtqwy"}),
                                  headers={"content-type": "application/json",
                                           "access-token": self.token})
        self.assertIn("Password is required", str(reset.data))

    def test_password_validation(self):
        """Test password must be 6-20 characters, alphanumeric"""
        reset = self.client().put('/api/v1/auth/reset-password',
                                  data=json.dumps(
                                      {"password": "123", "old_password": "qwtqwy"}),
                                  headers={"content-type": "application/json",
                                           "access-token": self.token})
        self.assertEqual(reset.status_code, 406)
        self.assertIn(
            "Password must be 6-20 Characters and can only contains leters",
            str(reset.data)
        )

    def test_wrong_old_password(self):
        """Test old password is required to change password"""
        reset = self.client().put('/api/v1/auth/reset-password',
                                  data=json.dumps(
                                      {"password": "qwertyu123", "old_password": "qwtqwy"}),
                                  headers={"content-type": "application/json",
                                           "access-token": self.token})
        self.assertEqual(reset.status_code, 406)
        self.assertIn("Wrong old Password", str(reset.data))

    def test_all_fileds_required(self):
        """Test password, oldpassword are required to change password"""
        reset = self.client().put('/api/v1/auth/reset-password',
                                  data=json.dumps({"password": "qwertyu123"}),
                                  headers={"content-type": "application/json",
                                           "access-token": self.token})
        self.assertEqual(reset.status_code, 400)
        self.assertIn("check you are sending correct information",
                      str(reset.data))
