import unittest
import os
import json
from app import create_app
from app.models.v2 import Business, User


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
        self.empy_business = {
            "name": "",
            "location": "",
            "category": "",
            "bio": ""
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
        Business.query.delete()
        User.query.delete()

    def test_business_can_create_successfully(self):
        """Tests that a business can be created successfully"""
        initial_count = len(Business.query.all())
        res = self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        final_count = len(Business.query.all())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)
        self.assertIn("Business created", str(res.data))

    def test_cannot_create_duplicate(self):
        """Tests that no two businesses can exist with similar name"""
        self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        res2 = self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res2.status_code, 401)
        self.assertIn("Sorry!! name taken!", str(res2.data))

    def test_cannot_create_with_name(self):
        """
        Tests that business name location and category
        must be provided to create an new business
        """
        res = self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.empy_business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertIn("Field cannot be empty", str(res.data))
        
    # test the home url renders the documentation template
    def test_documentation_render(self):
        rv = self.client().get('/')
        self.assertIn('WeConnect :: API v2', str(rv.data))