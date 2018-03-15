import unittest
import os
import json
from app import create_app
from app.v1 import business_model, user_model


class LoginUserTestCase(unittest.TestCase):
    """This class implements Login user TestCases"""

    def setUp(self):
        """Will be called before every test"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {"username": "miriti", "password": "qwerty123!@#",
                     "first_name": "eric", "last_name": "Miriti"}
        self.logins = {"username": "miriti", "password": "qwerty123!@#"}
        # Create_user
        self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                           headers={"content-type": "application/json"})

    def tearDown(self):
        """ clear data after every test"""
        user_model.users.clear()

    def test_user_can_login(self):
        """Test user can login to get access token"""
        login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token",str(login.data))

    def test_cannot_login_if_not_registered(self):
        """ Test that only registered users can login"""
        user_model.users.clear()  # clears users
        login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 401)
        self.assertIn("Username not found!",str(login.data))

    def test_login_details_required(self):
        """Test that all login fields are required"""
        login = self.client().post('/api/v1/auth/login', 
                        data=json.dumps({"username": "", "password": "11313"}),
                        headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 401)
        self.assertIn("login required!",str(login.data))

    def test_bad_request_with_wrong_filds(self):
        """tests app will only accept required parameters"""
        login = self.client().post('/api/v1/auth/login', data=json.dumps({"password": "11313"}),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 400)
        self.assertIn("check you are sending correct information",str(login.data))

 
if __name__ == "__main__":
    unittest.main()
