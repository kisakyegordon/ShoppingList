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

    def test_already_registered_user(self):

        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)

        second_res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)

        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists. Please login.")

    def test_login(self):
        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }
        reg = self.client().post('/auth/register', data=self.user_login)
        log = self.client().post('/auth/login', data=self.user_login)

        result = json.loads(log.data.decode())
        self.assertTrue(result['access_token'])
        self.assertEqual(result['message'], "Successfully LoggedIn")
        self.assertEqual(log.status_code, 200)

    def test_unauthorised_login(self):

        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }
        log = self.client().post('/auth/login', data=self.user_login)

        result = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 401)





