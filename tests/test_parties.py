# Third party and local imports
import unittest
import json
from app import create_app, database_config

class TestPartyEndPoint(unittest.TestCase):
    '''This is a class that holds all methods for testing party endpoints'''
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        database_config.init_test_db()

        self.data={
            'name': 'Jubilee Party',
            'hqAddress' : 'Jubilee House, Nairobi',
            'logoUrl' : 'https://images.pexels.com/photos/866351/pexels-photo-866351.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
        }

        self.data_2={
            'name': 'Naswa Party',
            'hqAddress' : 'Naswa House, Nairobi',
            'logoUrl' : 'https://images.pexels.com/photos/866351/pexels-photo-866351.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
        }
        self.bad_data={
            'name': 'Naswa Party',
            'hqAddress' : 'Naswa House, Nairobi',
            'logoUrl' : ''
        }
        self.bad_data2={
            'name': 'Naswa Party',
            'hqAddress' : '',
            'logoUrl' : 'https://images.pexels.com/photos/866351/pexels-photo-866351.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
        }
        self.edit_data={
            'name': 'Nasa Party'
        }
    def test_add_party(self):
        '''Test adding a party'''
        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.data_2), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.bad_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.bad_data2), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_get_parties(self):
        '''Test to get all parties'''
        response = self.client.get(path='/api/v2/parties', content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_get_a_party(self):
        '''Test to get a specific party'''
        response = self.client.get(path='/api/v2/parties/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_edit_a_party(self):
        '''Test to edit a specific party'''
        response = self.client.patch(path='/api/v2/parties/1/name', data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_a_party(self):
        '''Test to delete a specific party'''
        response = self.client.delete(path='/api/v2/parties/2', content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()
