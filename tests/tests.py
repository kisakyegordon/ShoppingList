
import unittest
import os
import json
from app import create_app, db
import time
import datetime


class ShoppingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.shoppinglist = {'name' : 'Monday List'}
        self.shoppinglist2 = {'name' : 'Tuesday List'}
        self.shoppinglist_item = {'name' : 'Food'}
        self.shoppinglist_item2 = {'name' : 'Toiletries'}

        with self.app.app_context():
            db.session.close()
            # db.drop.all()
            db.create_all()

    def register(self, email="test@gmail.com", password="test", country_town='trial'):
        user_data = {
            'email': email,
            'password': password,
            'country_town':country_town
        }
        return self.client().post('/auth/register', data=user_data)

    def login(self, email="test@gmail.com", password="test"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_registration(self):
        self.register()


    def test_shoppinglist_creation(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Monday', str(res.data))

    def test_get_shoppinglists_pagination(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']
    
        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        res2 = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist2)
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/shoppinglists/?limit=1&page=1', headers=dict(Authorization="Bearer " + access_token))
        self.assertNotIn('Tuesday', str(result.data))

    def test_get_shoppinglist_by_id(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Monday', str(res.data))

    def test_add_shoppinglist_item(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res2 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)
        self.assertIn('Food', str(res2.data))

    def test_delete_shoppinglist_item(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res2 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)
        self.assertIn('Food', str(res2.data))
        res3 = self.client().delete('/shoppinglists/1/items/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertNotIn('Food', str(res3.data))

    def test_edit_shoppinglist_item(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res2 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)
        self.assertIn('Food', str(res2.data))
        res3 = self.client().get('/shoppinglists/1/items/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Food', str(res3.data))
        res4 = self.client().put('/shoppinglists/1/items/1', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item2)
        self.assertIn('Toiletries', str(res4.data))

    def test_get_single_shoppinglist_item(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res2 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)
        res3 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item2)
        res4 = self.client().get('/shoppinglists/1/items/2', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Toiletries', str(res4.data))

    def test_editing_shoppinglist(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/shoppinglists/1', headers=dict(Authorization="Bearer " + access_token), data={'name':'Monday List Edited'})
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/shoppinglists/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Edited', str(res.data))

    def test_deleting_shoppinglist(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/shoppinglists/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/shoppinglists/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 404)


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()








