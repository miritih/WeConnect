import unittest
import json
from app import create_app
from app.models.v2 import Business, Review


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
            "description": "The better option"
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
        # register business for reviews
        bus = self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.response = json.loads(bus.data.decode('utf-8'))

    def tearDown(self):
        """ clear data after every test"""
        Review.query.delete()
        Business.query.delete()

    def test_review_not_found(self):
        """test cannot delete or update a review that dos not exist"""
        res = self.client().put(
            'api/v2/businesses/reviews/1',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        res2 = self.client().delete(
            'api/v2/businesses/reviews/1',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("Review does not exist", str(res.data))
        self.assertIn("Review does not exist", str(res2.data))

    def test_can_delete_review(self):
        """
        Test that reviews can
        be deleted and updated
        """
        res = self.client().post(
            'api/v2/businesses/' + str(
                self.response['Business']['id']) + '/reviews',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        review = json.loads(res.data.decode('utf-8'))
        res1 = self.client().put(
            'api/v2/businesses/reviews/' + str(review['Review']['id']),
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        res3 = self.client().delete(
            'api/v2/businesses/reviews/' + str(review['Review']['id']),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        # self.assertEqual(res.status_code, 401)
        self.assertIn("Review Updated", str(res1.data))
        self.assertIn("Review deleted successfully", str(res3.data))

    def test_can_only_delete_own_reviews(self):
        """Tests that users cannot delete other users reviews"""
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps({
                "username": "mwenda5",
                "email": "ericmwenda55@gmail.com",
                "password": "qwerty123!@#",
                "first_name": "eric",
                "last_name": "Miriti"
            }),
            content_type='application/json'
        )
        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps({
                "username": "mwenda5",
                "password": "qwerty123!@#"
            }),
            content_type='application/json'
        )
        token = json.loads(login.data.decode("utf-8"))
        res = self.client().post(
            'api/v2/businesses/' + str(
                self.response['Business']['id']) + '/reviews',
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": token['auth_token']
            }
        )
        review = json.loads(res.data.decode('utf-8'))
        res1 = self.client().put(
            'api/v2/businesses/reviews/' + str(review['Review']['id']),
            data=json.dumps(self.review),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        res2 = self.client().delete(
            'api/v2/businesses/reviews/' + str(review['Review']['id']),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("you can only Update your reviews", str(res1.data))
        self.assertIn("you can only delete your reviews", str(res2.data))
