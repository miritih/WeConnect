import unittest
import os
import json
from app import create_app
from app.models.v2 import Business, Review, User


class AddBusinessTestCase(unittest.TestCase):
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

        self.business = {
            "name": "Safaricom",
            "location": "Nairobi,Kenya",
            "category": "Telecommunication",
            "bio": "The better option"
        }
        self.review = {
            "review": "Awesome Awesome Awesome ",
            "title": "Awesome title"
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

        self.data = json.loads(self.login.data.decode("utf-8"))

        # get the token to be used by tests
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        Review.query.delete()
        Business.query.delete()

    def test_can_add_review(self):
        """Test can add review successfully"""
        # register business for reviews
        bus = self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        response = json.loads(bus.data.decode('utf-8'))
        res = self.client().post(
            'api/v2/businesses/' + str(response['Business']['id']) + '/reviews',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("Your Review was added", str(res.data))
        self.assertEqual(res.status_code, 201)

    def test_review_for_non_existing_business(self):
        """Test cannot post review for a non existing business"""
        res = self.client().post(
            'api/v2/businesses/43/reviews',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("Business not found", str(res.data))
