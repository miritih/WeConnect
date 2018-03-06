import unittest
import os
import json
from app import create_app, user_model


class CreateUserTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {"username": "miriti", "password": "123",
                     "first_name": "eric", "last_name": "Miriti"}

    def tearDown(self):
        """ clear data after every test"""
        user_model.users.clear()

    def test_user_creation(self):
        """
        Test API can create a user (POST request)
        """
        initial_count = len(user_model.users)
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                                 headers={"content-type": 'application/json'})
        final_count = len(user_model.users)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)

    def test_cannot_create_duplicate_user(self):
        """
        Tests that duplicate usernames cannot be created
        """
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                                 content_type='application/json')
        res2 = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                                  content_type='application/json')
        assert b'{\n  "message": "Sorry!! Username taken!"\n}\n' in res2.data

if __name__ == "__main__":
    unittest.main()
