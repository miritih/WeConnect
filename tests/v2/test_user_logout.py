import unittest
import json
from app import create_app
from app.models.v2 import User


class LogoutUserTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app('testing')
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
        self.register = self.client().post(
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
        print(self.data)
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        User.query.delete()

    def test_user_can_logout(self):
        """Tests users can logout"""
        logout = self.client().post(
            '/api/v2/auth/logout',
            data={},
            headers={
                "content_type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(logout.status_code, 200)

    def test_user_needs_token_to_logout(self):
        """test that you must be logged for you to logout"""
        res = self.client().post(
            '/api/v2/auth/logout',
            data={},
            headers={"content_type": "application/json"}
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("Token is missing, login to get token", str(res.data))

    def test_invalid_token(self):
        """Test cannot accept invalid token"""
        logout = self.client().post( 
            '/api/v2/auth/logout',
            data={},
            headers={
                "content_type": "application/json",
                "access-token": "wyuweyguy1256"
            }
        )
        self.assertEqual(logout.status_code, 401)
        self.assertIn("Token is invalid or Expired!", str(logout.data))

    def test_is_logged_out(self):
        """Test user is logged out"""
        self.client().post(
            '/api/v2/auth/logout',
            headers={
                "content_type": "application/json",
                "access-token": self.token
            }
        )
        logout = self.client().post(
            '/api/v2/auth/logout',
            headers={
                "content_type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(logout.status_code, 401)
        self.assertIn("You are not logged in", str(logout.data))
