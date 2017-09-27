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

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()








