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
        self.business = {"name": "Andela", "Location": "Nairobi,Kenya",
                         "category": "Tech", "Bio": "Epic"}

    def tearDown(self):
        """ clear data after every test"""
        business_model.businesses.clear()

    def test_business_can_create_successfully(self):
        """Tests that a business can be crated successfully"""
        initial_count = len(business_model.businesses)
        res = self.client.post('/api/v1/businesses', data=json.dumps(self.business),
                               headers={"content-type": "application/json"})
        final_count = len(business_model.businesses)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)

    def test_cannot_create_duplicate(self):
        """Tests that no two businesses can exist with similar name"""
        res = self.client.post('/api/v1/businesses', data=json.dumps(self.business),
                               headers={"content-type": "application/json"})
        res2 = self.client.post('/api/v1/businesses', data=json.dumps(self.business),
                                headers={"content-type": "application/json"})

        assert b'{\n  "message": "Sorry!! Name taken!"\n}\n' in res2.data

    def test_cannot_create_with_empty_data(self):
        """Tests that business name location and category must be provided to create an new business"""
        res = self.client.post('/api/v1/businesses', data=json.dumps({}),
                               headers={"content-type": "application/json"})
            assert b'{\n  "message": "Name must be available!"\n}\n' in res2.data
