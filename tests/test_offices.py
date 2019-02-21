# third party and local imports
import unittest
import json
from app import create_app, database_config

class TestOfficeEndPoint(unittest.TestCase):
    '''This is a test class for testing all office endpoints'''
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        database_config.destroy_db()
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

        self.userlogin = {
            'email' : 'admin@admin.com',
            'password' : 'password'
        }

    def create_admin(self):
        query = """INSERT INTO users (nationalid, firstname, lastname, othername, email, phonenumber, passporturl, password, isadmin) VALUES ('3363532211', 'Kimaiyo', 'Isaac', 'Kim', 'admin@admin.com', '0712345679', 'https://ppass.com', 'password', TRUE);"""
        con = database_config.init_test_db()
        cur = con.cursor()

        cur.execute(query)
        con.commit()
        con.close()


    def login_user(self):
        self.create_admin()
        response = self.client.post(path='/api/v2/auth/login', data=json.dumps(self.userlogin), content_type='application/json')
        token = response.json['token']

        return {"Authorization" : "Bearer " + token}

    def test_add_office(self):
        '''Test adding a new office'''
        response = self.client.post(path='/api/v2/offices',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v2/offices',data=json.dumps(self.data_2), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v2/offices',data=json.dumps(self.data_3), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 201)
        
        response = self.client.post(path='/api/v2/offices',data=json.dumps(self.bad_data), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v2/offices',data=json.dumps(self.bad_data2), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v2/offices',data=json.dumps(self.bad_data3), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v2/offices',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 409)

        response = self.client.post(path='/api/v2/offices/1/register', data=json.dumps(self.candidate), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 201)
        
    def test_get_offices(self):
        '''Test to get all offices'''
        self.client.post(path='/api/v2/offices',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.get(path='/api/v2/offices', content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)
        
    def test_get_an_office(self):
        '''Test to get a specific office'''
        self.client.post(path='/api/v2/offices',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.get(path='/api/v2/offices/1', content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)
        
    def test_edit_an_office(self):
        '''Test to edit a specific political office'''
        self.client.post(path='/api/v2/offices',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.patch(path='/api/v2/offices/1', data=json.dumps(self.edit_office), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)

    def test_delete_an_office(self):
        '''Test for deleting a specific office'''
        self.client.post(path='/api/v2/offices',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.delete(path='/api/v2/offices/1', content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)

    def register_a_candidate(self):
        '''Test for user to register as a candidate'''
        self.client.post(path='/api/v2/offices',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.post(path='/api/v2/offices/1/register', data=json.dumps(self.candidate), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()