import unittest
import os
import json
from app import create_app, business_model


class AddBusinessTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        self.user = {"username": "miriti", "password": "123",
                     "first_name": "eric", "last_name": "Miriti"}

        self.logins = {"username": "miriti", "password": "123"}

        self.business = {"name": "Andela", "location": "Nairobi,Kenya",
                         "category": "Tech", "bio": "Epic"}
        self.review = {"review": "Awesome Awesome Awesome "}

        self.client().post('/api/v1/auth/register', data=json.dumps(self.user),
                           content_type='application/json')

        self.login = self.client().post('/api/v1/auth/login', data=json.dumps(self.logins),
                                        content_type='application/json')

        self.data = json.loads(self.login.data.decode("utf-8"))

        # get the token to be used by tests
        self.token = self.data['auth_token']

        # register business for reviews
        self.client().post('/api/v1/businesses', data=json.dumps(self.business),
                           headers={"content-type": "application/json", "access-token": self.token})

    def tearDown(self):
        """ clear data after every test"""
        business_model.businesses.clear()

    def test_can_add_review(self):
        """Test can add review successfully"""
        res = self.client().post('api/v1/businesses/1/reviews', data=json.dumps(self.review),
                                 headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res.status_code, 201)

    def test_review_for_non_existing_business(self):
        """Test cannot post review for a non existing business"""
        res = self.client().post('api/v1/businesses/43/reviews', data=json.dumps(self.review),
                                 headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res.status_code, 401)
        assert b'{\n  "message": "Business not found"\n}\n' in res.data
