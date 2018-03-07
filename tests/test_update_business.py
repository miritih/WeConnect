import unittest
import os
import json
from app import create_app, business_model


class CreateUserTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {
            "username": "miriti",
            "password": "123",
            "first_name": "eric",
            "last_name": "Miriti"
        }

        self.logins = {"username": "miriti", "password": "123"}

        self.business = {
            "name": "Andela",
            "location": "Nairobi,Kenya",
            "category": "Tech",
            "bio": "Epic"
        }
        self.update_business = {
            "name": "",
            "location": "",
            "category": "",
            "bio": ""
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

    def test_business_can_updated_successfully(self):
        """Tests that a business can be updated successfully"""
        res = self.client().post('/api/v1/businesses', data=json.dumps(self.business),
                                 headers={"content-type": "application/json", "access-token": self.token})
        res2 = self.client().put('/api/v1/businesses/1', data=json.dumps(self.update_business),
                                 headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res2.status_code, 200)

    def can_can_get_businesses(self):
        """test can get all busineses"""
        res = self.client().get('/api/v1/businesses',
                                headers={"access-token": self.token})
        self.assertEqual(res.status_code, 200)

    def test_can_only_update_own_business(self):
        """ Tests that user cannot update other users businesses"""

        pass
