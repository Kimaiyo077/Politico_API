import unittest
import json
from app import create_app

class TestOfficeEndPoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.data={
            'id' : 1,
            'name': 'Presidential',
            'type': 'State Government'
        }

        self.data_2={
            'id' : 2,
            'name': 'Governor',
            'type': 'Local Government'
        }

        
        self.data_3={
            'id' : 3,
            'name': 'MP',
            'type': 'Local Government'
        }

        self.edit_office={
            'name' : 'Senetor'
        }

    def test_add_office(self):
        '''Test adding a new office'''
        response = self.client.post(path='/api/v1/addoffices',data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v1/addoffices',data=json.dumps(self.data_2), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v1/addoffices',data=json.dumps(self.data_3), content_type='application/json')
        self.assertEqual(response.status_code, 201)

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
        response = self.client.delete(path='/api/v1/office/3', content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()