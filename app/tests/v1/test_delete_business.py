import unittest
import os
import json
from app import create_app
from app.v1.v1 import business_model, user_model

class DeleteBusinessTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {
            "username": "miriti",
            "password": "qwerty123!@#",
            "first_name": "eric",
            "last_name": "Miriti"
        }

        self.logins = {"username": "miriti", "password": "qwerty123!@#"}

        self.business = {
            "name": "Andela",
            "location": "Nairobi,Kenya",
            "category": "Tech",
            "bio": "Epic"
        }
        self.client().post(
            '/api/v1/auth/register',
            data=json.dumps(self.user),
            content_type='application/json'
        )

        self.login = self.client().post(
            '/api/v1/auth/login',
            data=json.dumps(self.logins),
            content_type='application/json'
        )
        self.data = json.loads(self.login.get_data(as_text=True))
        # get the token to be used by tests
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        business_model.businesses.clear()

    def test_can_delete_successfully(self):
        """Tests that a business can be Deleted successfully"""
        res = self.client().post('/api/v1/businesses', data=json.dumps(self.business),
                                 headers={"content-type": "application/json", "access-token": self.token})
        res2 = self.client().delete('/api/v1/businesses/1',
                                    headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res2.status_code, 201)
        self.assertIn("Business Deleted",str(res2.data))

    def test_cannot_delete_empty(self):
        """Tests that cannot delete a business that doesn't exist"""
        res2 = self.client().delete('/api/v1/businesses/1',
                                    headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res2.status_code, 401)
        self.assertIn("Business not found",str(res2.data))

    def can_only_delete_own_business(self):
        """test that one can only delete a business they created """
        res2 = self.client().delete('/api/v1/businesses/1',
                                    headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res2.status_code, 401)
        assert b'{\n  "message": "Sorry! You can only delete your business!!"\n}\n' in res2.data
    
    def test_can_only_delete_own_business(self):
        """Tests that users cannot delete other users businesses"""
        business_model.add_businesses("name",
                    "location", "category", "bio", "kenneth")
        res2 = self.client().delete('/api/v1/businesses/1',
                                 headers={"content-type": "application/json",
                                          "access-token": self.token})
        self.assertEqual(res2.status_code, 401)
        self.assertIn("Sorry! You can only delete your business",str(res2.data))
