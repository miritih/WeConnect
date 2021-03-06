import unittest
import os
import json
from app import create_app
from app.v1.v1 import business_model


class AddBusinessTestCase(unittest.TestCase):
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

        self.business = {"name": "Safaricom", "location": "Nairobi,Kenya",
                         "category": "Telecommunication", "bio": "Epic"}
        self.empy_business = {"name": "", "location": "",
                              "category": "", "bio": ""}
        self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                           content_type='application/json')

        self.login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                        content_type='application/json')
        self.data = json.loads(self.login.data.decode("utf-8"))
        # get the token to be used by tests
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        business_model.businesses.clear()

    def test_business_can_create_successfully(self):
        """Tests that a business can be created successfully"""
        initial_count = len(business_model.businesses)
        res = self.client().post('/api/v1/businesses', data=json.dumps(self.business),
                                 headers={"content-type": "application/json", "access-token": self.token})
        final_count = len(business_model.businesses)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)
        self.assertIn("Business created",str(res.data))

    def test_cannot_create_duplicate(self):
        """Tests that no two businesses can exist with similar name"""
        res = self.client().post('/api/v1/businesses',
                    data=json.dumps(self.business),
                    headers={
                        "content-type": "application/json",
                        "access-token": self.token
                    })
        res2 = self.client().post('/api/v1/businesses', data=json.dumps(self.business),
                                  headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res2.status_code, 401)
        assert b'{\n  "message": "Sorry!! Name taken!"\n}\n' in res2.data
 
    def test_cannot_create_with_name(self):
        """Tests that business name location and category must be provided to create an new business"""
        res = self.client().post('/api/v1/businesses', data=json.dumps(self.empy_business),
                                 headers={"content-type": "application/json", "access-token": self.token})
        assert b'{\n  "message": "Name cannot be empty!"\n}\n' in res.data
