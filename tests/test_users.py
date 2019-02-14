import unittest
import json
from app import create_app, database_config

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        database_config.destroy_db()
        database_config.init_test_db()

        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user1 = {
            'nationalId' : '321654987',
            'firstname' : 'Isaack',
            'lastname' : 'Kimaiyo',
            'othername' : 'Kibiwot',
            'email' : 'email@email.com',
            'phoneNumber': '9876543210',
            'passportUrl' : 'passport.com'
        }

        self.duplicate_user = {
            'nationalId' : '321654987',
            'firstname' :'Isaac',
            'lastname' : 'Kimaiyo',
            'othername' : 'Kibiwot',
            'email' : 'email@email.com',
            'phoneNumber': '9876543210',
            'passportUrl' : 'passport.com'
        }

    def test_create_account(self):
        response = self.client.post(path='/api/v2/auth/signup',content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post(path='/api/v2/auth/signup',data=json.dumps(self.user1), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post(path='/api/v2/auth/signup',data=json.dumps(self.duplicate_user), content_type='application/json')
        self.assertEqual(response.status_code, 409)

    
    if __name__=='__main__':
        unittest.main()