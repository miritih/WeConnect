import unittest
import json
from app import create_app
from app.models.v2 import Business


class DeleteBusinessTestCase(unittest.TestCase):
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
            "category": "Tech",
            "description": "Epic"
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

    def test_can_delete_successfully(self):
        """Tests that a business can be Deleted successfully"""
        self.client().post(
            '/api/v2/businesses',
            data=json.dumps(self.business),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            })
        bsid = Business.query.first()  # Get the last created Record
        res2 = self.client().delete(
            '/api/v2/businesses/' + str(bsid.id),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            })

        self.assertEqual(res2.status_code, 201)
        self.assertIn("Business Deleted", str(res2.data))

    def test_cannot_delete_empty(self):
        """Tests that cannot delete a business that doesn't exist"""
        res2 = self.client().delete(
            '/api/v2/businesses/1',
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res2.status_code, 401)
        self.assertIn("Business not found", str(res2.data))

    def can_only_delete_own_business(self):
        """test that one can only delete a business they created """
        res2 = self.client().delete(
            '/api/v2/businesses/1',
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res2.status_code, 401)
        self.assertIn(
            "Sorry! You can only delete your business!!", str(res2.data))

    def test_can_only_delete_own_business(self):
        """Tests that users cannot delete other users businesses"""
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps({
                "username": "Miritim",
                "email": "ericmwenda552@gmail.com",
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
        res2 = self.client().delete(
            '/api/v2/businesses/' + str(response['Business']['id']),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEqual(res2.status_code, 401)
        self.assertIn("Sorry! You can only delete your business",
                      str(res2.data))
