# Third party and local imports
import unittest
import json
from app import create_app, database_config

class TestPartyEndPoint(unittest.TestCase):
    '''This is a class that holds all methods for testing party endpoints'''
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        database_config.destroy_db()
        database_config.init_test_db()

        self.userlogin={
            'email' : 'admin@admin.com',
            'password' : 'password'
        }

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
    
    def create_admin(self):
        query = """INSERT INTO users (nationalid, firstname, lastname, othername, email, phonenumber, passporturl, password, isadmin) VALUES ('33635322', 'Kimaiyo', 'Isaac', 'Kim', 'admin@admin.com', '0712345679', 'https://ppass.com', 'password', TRUE);"""
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

    def test_add_party(self):
        '''Test adding a party'''
        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.data_2), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 201)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.bad_data), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.bad_data2), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 409)

    def test_get_parties(self):
        '''Test to get all parties'''
        self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.get(path='/api/v2/parties', content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)
    
    def test_get_a_party(self):
        '''Test to get a specific party'''
        self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.get(path='/api/v2/parties/1', content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)

    def test_edit_a_party(self):
        '''Test to edit a specific party'''
        self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.patch(path='/api/v2/parties/1/name', data=json.dumps(self.edit_data), content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)

    def test_delete_a_party(self):
        '''Test to delete a specific party'''
        self.client.post(path='/api/v2/parties',data=json.dumps(self.data), content_type='application/json', headers=self.login_user())
        response = self.client.delete(path='/api/v2/parties/1', content_type='application/json', headers=self.login_user())
        self.assertEqual(response.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()
