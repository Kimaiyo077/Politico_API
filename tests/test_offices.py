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

    def test_add_office(self):
        pass
    def test_get_offices(self):
        '''Test to get all offices'''
        response = self.client.get(path='/api/v1/offices', content_type='application/json')
        self.assertEqual(response.status_code, 200)
    def test_get_an_office(self):
        pass
    def test_edit_an_office(self):
        pass
    def test_delete_an_office(self):
        pass

if __name__ == '__main__':
    unittest.main()