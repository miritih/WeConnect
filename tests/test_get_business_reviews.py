import unittest
import os
import json
from app import create_app, business_model, review_model


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
        review_model.reviews.clear()

    def test_can_get_business_reviews(self):
        review_model.reviews.clear()
        """Test can get all business reviews successfully"""
        self.client().post('api/v1/businesses/1/reviews', data=json.dumps(self.review),
                           headers={"content-type": "application/json", "access-token": self.token})
        self.client().post('api/v1/businesses/1/reviews', data=json.dumps(self.review),
                           headers={"content-type": "application/json", "access-token": self.token})
        res = self.client().get('api/v1/businesses/1/reviews',
                                headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(review_model.reviews), 2)
