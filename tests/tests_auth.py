import unittest
import json
import time
from app import create_app, db
from app.models import User



class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")

        self.client = self.app.test_client

        self.base_register = '/api/v2/auth/register'
        self.base_login = '/api/v2/auth/login'
        self.base_logout = '/api/v2/auth/logout'
        self.base_reset = '/api/v2/auth/reset-password'

        self.user_data = {
            'email': 'joe@gmail.com',
            'password': 'joe',
            'country_town': 'trial'
        }

        self.user_data_error = {
            'email': 'joe@gmail.com',
            'password': 'joe'
        }

        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }

        self.user_login2 = {
            'email': 'joe@gmail.com',
            'password' : 'new-joe'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()


    def test_registration(self):
        res = self.client().post(self.base_register, data=self.user_data)

        result = json.loads(res.data.decode())

        self.assertEqual(result['message'], "You registered successfully.")
        self.assertEqual(res.status_code, 201)

    def test_registration_no_data(self):
        res = self.client().post(self.base_register, data="")

        result = json.loads(res.data.decode())

        self.assertEqual(result['message'], "Enter your user login details")
        self.assertEqual(res.status_code, 400)

    def test_registration_missing_data(self):
        res = self.client().post(self.base_register, data=self.user_data_error)
        self.assertEqual(res.status_code, 400)

    def test_already_registered_user(self):

        res = self.client().post(self.base_register, data=self.user_data)
        self.assertEqual(res.status_code, 201)

        second_res = self.client().post(self.base_register, data=self.user_data)
        self.assertEqual(second_res.status_code, 409)

        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User Already Exists. Please Login.")

    def test_login(self):
        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }
        reg = self.client().post(self.base_register, data=self.user_data)
        log = self.client().post(self.base_login, data=self.user_login)

        result = json.loads(log.data.decode())
        self.assertTrue(result['access_token'])
        self.assertEqual(result['message'], "Successfully LoggedIn")
        self.assertEqual(log.status_code, 200)

    def test_logout(self):
        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }
        
        reg = self.client().post(self.base_register, data=self.user_data)
        log = self.client().post(self.base_login, data=self.user_login)

        res = self.client().post(self.base_logout, headers=dict(Authorization="Bearer " + json.loads(log.data.decode())['access_token']))

        data = json.loads(res.data.decode())
        self.assertTrue(data['message'] == 'Logged Out Successfully')
        self.assertEqual(res.status_code, 200)
        

    def test_unauthorised_login(self):

        log = self.client().post(self.base_login, data=self.user_login)

        result = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 400)

    def test_reset_password(self):
        data = {
            'email': 'joe@gmail.com',
            'password': 'new-joe',
            'country_town': 'trial'
        }

        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }

        self.user_login2 = {
            'email': 'joe@gmail.com',
            'password' : 'new-joe'
        }
        reg = self.client().post(self.base_register, data=self.user_data)
        log = self.client().post(self.base_login, data=self.user_login)

        res = self.client().post(self.base_reset, data=data)
        data = json.loads(res.data)
        self.assertTrue(data['message'] == 'Password Succesfully Changed')

        log1 = self.client().post(self.base_login, data=self.user_login)
        data1 = json.loads(log1.data.decode())
        self.assertTrue(data1['message'] == 'Invalid email or password')

        log2 = self.client().post(self.base_login, data=self.user_login2)
        result = json.loads(log.data.decode())
        self.assertTrue(result['access_token'])
        self.assertEqual(result['message'], "Successfully LoggedIn")
        self.assertEqual(log.status_code, 200)

    def test_reset_password_no_user(self):
        self.data = {
            'email': 'max@gmail.com',
            'password': 'new-joe',
            'country_town': 'trial'
        }

        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }

        self.user_login2 = {
            'email': 'joe@gmail.com',
            'password' : 'new-joe'
        }
        reg = self.client().post(self.base_register, data=self.user_data)
        log = self.client().post(self.base_login, data=self.user_login)

        res = self.client().post(self.base_reset, data=self.data)
        self.assertTrue(res.status_code, 404)
        data = json.loads(res.data)
        self.assertTrue(data['message'] == 'No User Found')




        





