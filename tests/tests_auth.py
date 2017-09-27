import unittest
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")

        self.client = self.app.test_client

        self.user_data = {
            'email': 'test@sample.com',
            'password': 'test_password'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()


    def test_registration(self):
        res = self.client().post('/auth/register', data=self.user_data)

        result = json.loads(res.data.decode())

        self.assertEqual(result['message'], "You registered successfully.")
        self.assertEqual(res.status_code, 201)





