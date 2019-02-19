# third party and local imports
import unittest
import json
from app import create_app, database_config

class TestOfficeEndPoint(unittest.TestCase):
    '''This is a test class for testing all office endpoints'''
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        database_config.init_test_db() 

        self.data={
            'name': 'Presidential',
            'type': 'Federal'
        }

        self.data_2={
            'name': 'Governor',
            'type': 'Local Government'
        }

        self.data_3={
            'name': 'Parliament',
            'type': 'Local Government'
        }

        self.edit_office={
            'name' : 'Senetor'
        }

        self.bad_data={
            'name' : '',
            'type' : 'office' 
        }

        self.bad_data2={
            'name' : 'Environment',
            'type' : ''
        }

        self.bad_data3={
            'name': 'Presidential',
            'type': 'Presidents office'
        }

        self.candidate={
            "user_id" : 1 
        } 

    def test_add_office(self):
        '''Test adding a new office'''
        response = self.client.post(path='/api/v1/offices',data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v1/offices',data=json.dumps(self.data_2), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v1/offices',data=json.dumps(self.data_3), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response = self.client.post(path='/api/v1/offices',data=json.dumps(self.bad_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v1/offices',data=json.dumps(self.bad_data2), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v1/offices',data=json.dumps(self.bad_data3), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v1/offices',data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        
    def test_get_offices(self):
        '''Test to get all offices'''
        response = self.client.get(path='/api/v1/offices', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
    def test_get_an_office(self):
        '''Test to get a specific office'''
        response = self.client.get(path='/api/v1/offices/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
    def test_edit_an_office(self):
        '''Test to edit a specific political office'''
        response = self.client.patch(path='/api/v1/offices/2', data=json.dumps(self.edit_office), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_an_office(self):
        '''Test for deleting a specific office'''
        response = self.client.delete(path='/api/v1/offices/3', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_register_a_candidate(self):
        '''Test for registering a new candidate'''
        response = self.client.post(path='/api/v1/offices/1/register', data=json.dumps(self.candidate), content_type='application/json')
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()