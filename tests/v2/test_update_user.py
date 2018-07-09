import unittest
import json
from app import create_app
from app.models.v2 import User


class UpdateUserTestCase(unittest.TestCase):
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
        self.updateUser = {
            "email": "ericmwenda5@gmail.com",
            "first_name": "kaibi",
            "last_name": "Miriti",
            "image": "avatar_2x.png"
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

    def test_can_update_user(self):
        """Tests users can update password"""
        update = self.client().put(
            '/api/v2/auth/update-profile',
            data=json.dumps(self.updateUser),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("user updated", str(update.data))

    def test_reured_filds(self):
        """tests password must be given"""
        reset = self.client().put(
            '/api/v2/auth/update-profile',
            data=json.dumps({
                "email": "ericmwenda5@gmail.com",
                "first_name": "kaibi"
            }),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("required field", str(reset.data))
