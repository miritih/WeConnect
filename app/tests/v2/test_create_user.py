import unittest
import os
import json
from app import create_app
from app.models.v2 import User


class CreateUserTestCase(unittest.TestCase):
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

    def tearDown(self):
        """ clear data after every test"""
        User.query.delete()

    def test_user_creation(self):
        """
        Test API can create a user (POST request)
        """
        initial_count = len(User.query.all())
        res = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        final_count = len(User.query.all())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)

    def test_cannot_create_duplicate_user(self):
        """
        Tests that duplicate usernames cannot be created
        """
        res = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        res2 = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        self.assertIn("Sorry!! Username taken!", str(res2.data))

    def test_details_missing(self):
        """test username and password required"""
        res = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps({
                "first_name": "eric",
                "last_name": "Miriti"
            }),
            headers={"content-type": 'application/json'}
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("required field", str(res.data))

    def test_email_cannot_duplicate(self):
        """Test cannot create duplicate emmails"""
        res = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        res2 = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        self.assertEqual(res2.status_code, 401)
        self.assertIn("Sorry!! Email taken!", str(res2.data))

    def test_password_validation(self):
        """Test password must be 6-20 characters, alphanumeric"""
        res = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps({
                "username": "mwenda",
                "eric@gmail.com"
                "password": "123",
                "first_name": "Miriti",
                "last_name": "eric"
            }),
            headers={"content-type": 'application/json'}
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn(
            "Password must be 6 - 20 Characters and can only contains leters",
            str(res.data)
        )

if __name__ == "__main__":
    unittest.main()
