from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-type': 'application/json'})

                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')

                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():

                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'id': 1, 'name': 'test', 'price': 19.99},
                                 json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'price': 19.99},
                                     json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'},
                                     json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():

                resp = client.delete('/item/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                 json.loads(resp.data))

    def test_put_item_update(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)

                resp = client.put('/item/test', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 18.99)
                self.assertDictEqual({'id': 1, 'name': 'test', 'price': 18.99},
                                     json.loads(resp.data))

    def test_put_item_new(self):
        with self.app() as client:
            with self.app_context():

                resp = client.put('/item/test', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 18.99)
                self.assertDictEqual({'id': 1, 'name': 'test', 'price': 18.99},
                                     json.loads(resp.data))

    def test_list_item(self):
        with self.app() as client:
            with self.app_context():

                StoreModel('test')
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/items')
                self.assertEqual({'items': [{'id': 1, 'name': 'test', 'price': 19.99}]},
                                 json.loads(resp.data))

    def test_list_item_empty(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/items')
                self.assertEqual({'items': []}, json.loads(resp.data))

