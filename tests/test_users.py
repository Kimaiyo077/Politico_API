import unittest
import json
from app import create_app, database_config

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        database_config.destroy_db()
        database_config.init_test_db()

        self.app = create_app('testing')
        self.client = self.app.test_client()

        user1 = {
            'firstname' :'Isaac',
            'lastname' : 'Kimaiyo',
            'othername' : 'Kibiwot',
            'email' : 'email@email.com',
            'password' :'123456789',
            'phoneNumber': '9876543210',
            'passportUrl' : 'passport.com'
        }

        duplicate_user = {
            'firstname' :'Isaac',
            'lastname' : 'Kimaiyo',
            'othername' : 'Kibiwot',
            'email' : 'email@email.com',
            'password' :'123456789',
            'phoneNumber': '9876543210',
            'passportUrl' : 'passport.com'
        }

    def test_create_account(self):
        response = self.client.post(path='/api/v2/auth/signup',data=json.dumps(self.user1), content_type='application/json')
        self.assertEqual(response.status_code, 201)