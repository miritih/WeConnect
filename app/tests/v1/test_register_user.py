import unittest
import os
import json
from app import create_app
from app.v1 import business_model, user_model


class CreateUserTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {"username": "miriti", "password": "qwerty123!@#",
                     "first_name": "eric", "last_name": "Miriti"}

    def tearDown(self):
        """ clear data after every test"""
        user_model.users.clear()

    def test_user_creation(self):
        """
        Test API can create a user (POST request)
        """
        initial_count = len(user_model.users)
        res = self.client().post('/api/v1/auth/register',
                                data=json.dumps(self.user),
                                headers={"content-type": 'application/json'})
        final_count = len(user_model.users)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)

    def test_cannot_create_duplicate_user(self):
        """
        Tests that duplicate usernames cannot be created
        """
        res = self.client().post('/api/v1/auth/register',
                                data=json.dumps(self.user),
                                content_type='application/json')
        res2 = self.client().post('/api/v1/auth/register', 
                                data=json.dumps(self.user),
                                content_type='application/json')
        assert b'{\n  "message": "Sorry!! Username taken!"\n}\n' in res2.data

    def test_details_missing(self):
        """test username and password required"""
        res = self.client().post('/api/v1/auth/register', data=json.dumps({
                                        "username": " ",
                                        "password": " ",
                                        "first_name": "eric",
                                        "last_name": "Miriti"
                                    }),
                                 headers={"content-type": 'application/json'})
        assert b'{\n  "message": "username or password missing"\n}\n' in res.data

    def test_bad_request(self):
        """test returns bad request if all fields not available"""
        res = self.client().post('/api/v1/auth/register',
                    data=json.dumps({"username": "mwenda", "last_name": "Miriti"}),
                    headers={"content-type": 'application/json'})
        self.assertEqual(res.status_code,400)
        self.assertIn("check you are sending correct information",str(res.data))
    
    def test_password_alidation(self):
        """Test password must be 6-20 characters, alphanumeric"""
        res = self.client().post('/api/v1/auth/register',
                    data=json.dumps({
                        "username": "mwenda",
                        "password":"123",
                        "first_name": "Miriti",
                        "last_name": "eric"
                    }),
                    headers={"content-type": 'application/json'})
        self.assertEqual(res.status_code, 406)
        self.assertIn(
           "Password must be 6-20 Characters",
            str(res.data)
            )

if __name__ == "__main__":
    unittest.main()
