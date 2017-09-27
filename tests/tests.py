import unittest
import os
import json
from app import create_app, db


class ShoppingTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.shoppinglist = {'name' : 'Monday List'}

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register(self, email="test@gmail.com", password="test"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login(self, email="test@gmail.com", password="test"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_shoppinglist_creation(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Monday', str(res.data))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()








