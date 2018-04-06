import unittest
import json
from app import create_app
from app.models.v2 import Business


class CreateUserTestCase(unittest.TestCase):
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
        self.update_business = {
            "name": "",
            "location": "Mombasa",
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
        self.data = json.loads(self.login.get_data(as_text=True))
        # get the token to be used by tests
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        Business.query.delete()

    def test_business_can_updated_successfully(self):
        """Tests that a business can be updated successfully"""
        self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        bsid = Business.query.first()
        res2 = self.client().put(
            '/api/v2/businesses/' + str(bsid.id),
            data=json.dumps(self.update_business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res2.status_code, 202)
        self.assertIn("business updated!", str(res2.data))

    def can_can_get_businesses(self):
        """test can get all busineses"""
        self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        res = self.client().get(
            '/api/v2/businesses',
            headers={"access-token": self.token}
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(Business.query.all()), 1)

    def test_bussiness_exists(self):
        """tests cannot get a buiness that does not exist"""
        res = self.client().get(
            '/api/v2/businesses/9212',
            headers={"access-token": self.token}
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("Business not found", str(res.data))

    def test_bussiness_name_taken(self):
        """tests cannot get a buiness that does not exist"""
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
        self.assertIn("Sorry!! Business name taken!", str(res2.data))

    def test_can_only_update_own_business(self):
        """Tests that users cannot update other users businesses"""
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps({
                "username": "Miritim",
                "email": "ericmwenda556@gmail.com",
                "password": "qwerty123!@#",
                "first_name": "eric",
                "last_name": "Miriti"
            }),
            content_type='application/json'
        )

        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps({
                "username": "Miritim",
                "password": "qwerty123!@#"
            }),
            content_type='application/json'
        )
        token = json.loads(login.data.decode("utf-8"))
        bs = self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": token['auth_token']
            }
        )
        response = json.loads(bs.data.decode('utf-8'))
        res2 = self.client().put(
            '/api/v2/businesses/' + str(response['Business']['id']),
            data=json.dumps(self.update_business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        # self.assertEqual(res2.status_code, 401)
        self.assertIn(
            "Sorry! You can only update your business",
            str(res2.data)
        )

    def test_can_get_business(self):
        """
        Tests that all registerd
        businesses can be retrived
        """
        initial_count = len(Business.query.all())
        self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        res = self.client().get(
            '/api/v2/businesses',
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        final_count = len(Business.query.all())
        response = json.loads(res.data.decode('utf-8'))
        self.assertEqual(final_count - initial_count, 1)
        self.assertEqual(len(response['objects']), 1)
