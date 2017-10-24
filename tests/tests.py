
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

    def test_shoppinglist_search(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)

        search = self.client().get('/shoppinglists/search/?q=mon', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Monday', str(search.data))

    def test_shoppinglist_getall(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        res2 = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist2)
        search = self.client().get('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Monday', str(search.data))
        self.assertIn('Tuesday', str(search.data))

    def test_shoppinglist_creation_no_entry(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data="")
        self.assertEqual(res.status_code, 400)
        response = json.loads(res.data.decode())
        self.assertTrue(response['message'], 'Please Enter Some Valid Content')



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

    def test_add_shoppinglist_item_no_entry(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res2 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data="")
        self.assertTrue(res2.status_code, 400)
        response = json.loads(res2.data.decode())
        self.assertTrue(response['message'], 'Please Enter Some Valid Content')

    def test_get_shoppinglist_items(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res2 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)
        self.assertIn('Food', str(res2.data))
        res3 = self.client().get('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)
        self.assertIn('Food', str(res3.data))


    def test_edit_non_existant_shoppinglist(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res3 = self.client().post('/shoppinglists/2/items/', headers=dict(Authorization="Bearer " + access_token),data=self.shoppinglist_item)
        response = json.loads(res3.data.decode())
        self.assertTrue(response['message'], 'List Does Not Exist')


    def test_edit_non_existant_shoppinglist_item(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res3 = self.client().get('/shoppinglists/1/items/1', headers=dict(Authorization="Bearer " + access_token))
        response = json.loads(res3.data.decode())
        self.assertTrue(response['message'], 'List Item Does Not Exist')
        

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
        response = json.loads(res4.data.decode())
        self.assertIn('Toiletries', response['name'])

    # All No Token Provided tests
    def test_decorator_messages(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', data=self.shoppinglist)
        response = json.loads(res.data.decode())
        self.assertTrue(response['message'], 'No Token Provided')

    def test_decorator_messages_no_token_lists(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)

        res2 = self.client().get('/shoppinglists/1')
        response = json.loads(res2.data.decode())
        self.assertTrue(response['message'], 'No Token Provided')

    def test_decorator_messages_no_token_post_list_item(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)

        res2 = self.client().post('/shoppinglists/1/items/',  data=self.shoppinglist)
        response = json.loads(res2.data.decode())
        self.assertTrue(response['message'], 'No Token Provided')

    def test_decorator_messages_no_token_post_list_item_modify(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)

        res2 = self.client().get('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)

        res3 = self.client().get('/shoppinglists/1/items/')      
        response = json.loads(res3.data.decode())
        self.assertTrue(response['message'], 'No Token Provided')

    # All Invalid Token Tests    

    def test_decorator_messages_invalid_token(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer "), data=self.shoppinglist)
        response = json.loads(res.data.decode())
        self.assertTrue(response['message'], 'Token is Invalid')

    def test_decorator_messages_invalid_token_lists(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)

        res2 = self.client().get('/shoppinglists/1', headers=dict(Authorization="Bearer "), data=self.shoppinglist)
        response = json.loads(res2.data.decode())
        self.assertTrue(response['message'], 'Token is Invalid')


    def test_decorator_messages_invalid_token_post_list_item(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)

        res2 = self.client().post('/shoppinglists/1/items/', headers=dict(Authorization="Bearer "), data=self.shoppinglist)
        response = json.loads(res2.data.decode())
        self.assertTrue(response['message'], 'Token is Invalid')

    def test_decorator_messages_invalid_token_post_list_item_modify(self):
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist)

        res2 = self.client().get('/shoppinglists/1/items/', headers=dict(Authorization="Bearer " + access_token), data=self.shoppinglist_item)

        res3 = self.client().get('/shoppinglists/1/items/', headers=dict(Authorization="Bearer "))      
        response = json.loads(res3.data.decode())
        self.assertTrue(response['message'], 'Token is Invalid')



    def test_unusable_token(self):
        self.user_login = {
            'email': 'joe@gmail.com',
            'password' : 'joe'
        }
        
        self.register()
        result = self.login()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/auth/logout', headers=dict(Authorization="Bearer " + access_token))

        data = json.loads(res.data.decode())
        self.assertTrue(data['message'] == 'Logged Out Successfully')
        self.assertEqual(res.status_code, 200)

        res1 = self.client().post('/shoppinglists/', headers=dict(Authorization="Bearer" + access_token), data=self.shoppinglist)
        response = json.loads(res1.data.decode())
        self.assertTrue(response['message'], 'Token is unusable - login again')

    def test_index_file(self):

        res = self.client().get('/')
        self.assertTrue(res.status_code, 200)




    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()








