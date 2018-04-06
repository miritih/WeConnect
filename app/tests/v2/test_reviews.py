import unittest
import json
from app import create_app
from app.models.v2 import Review


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
            "name": "Andela",
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

    def test_can_get_business_reviews(self):
        """Test can get all business reviews successfully"""
        bus = self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        response = json.loads(bus.data.decode('utf-8'))
        self.client().post(
            'api/v2/businesses/' + str(
                response['Business']['id']) + '/reviews',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.client().post(
            'api/v2/businesses/' + str(
                response['Business']['id']) + '/reviews',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        res = self.client().get(
            'api/v2/businesses/' + str(
                response['Business']['id']) + '/reviews',
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(Review.query.all()), 2)

    def test_no_reviews(self):
        """Test that a business has no reviews"""
        Review.query.delete()
        bus = self.client().post(
            '/api/v2/businesses',
            data=json.dumps({
                "name": "Andela Kenya",
                "location": "Nairobi,Kenya",
                "category": "Telecommunication",
                "bio": "The better option"
            }),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        response = json.loads(bus.data.decode('utf-8'))
        res = self.client().get(
            'api/v2/businesses/' + str(
                response['Business']['id']) + '/reviews',
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("No Reviews for this business", str(res.data))

    def test_business_not_exists(self):
        """
        Test to verify cannot get reviews
        for a business that does not exist
        """
        res = self.client().get(
            'api/v2/businesses/12893/reviews',
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("Business not found", str(res.data))
