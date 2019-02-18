import psycopg2
import datetime
import os
import jwt
from app import database_config

class BaseModel:
    def check_if_exists(table_name, field_name, value):
        con = database_config.init_test_db()
        cur = con.cursor()
        query = "SELECT * FROM {} WHERE {}= '{}';".format(table_name, field_name, value)
        cur.execute(query)
        res = cur.fetchall()

        if res:
            return True
        else:
            return False

    def auth_token_encoder(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
                'user': user_id
            }
            token = jwt.encode(
                payload,
                os.getenv('SECRET'),
                algorithm='HS256'
            )

            return token.decode()
        except Exception as e:
            return e

class userModel(BaseModel):
    
    def create_account(data):
        nationalId = data['nationalId'].strip()
        firstname = data['firstname'].strip()
        lastname = data['lastname'].strip()
        othername = data['othername'].strip()
        email = data['email'].strip()
        phoneNumber = data['phoneNumber'].strip()
        passportUrl = data ['passportUrl'].strip()
        password = data['password'].strip()

        token = ''

        if not nationalId:
            return [400 ,'national Id cannot be empty']
        elif not firstname:
            return [400 ,'First name cannot be empty']
        elif not lastname:
            return [400, 'Last name cannot be empty']
        elif not email:
            return [400, 'email cannot be empty']
        elif not password:
            return [400, 'password cannot be empty']
            
        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('users', 'nationalId', nationalId) == True:
            return [409, 'National Id already exists']
        elif BaseModel.check_if_exists('users', 'email', email) == True:
            return [409, 'That Email is in use already']

        new_user = {
            'nationalId' : nationalId,
            'firstname' : firstname,
            'lastname' : lastname,
            'othername' : othername,
            'email' : email,
            'phoneNumber' : phoneNumber,
            'passportUrl' : passportUrl,
            'password' : password
        }

        query = """ INSERT INTO users (nationalId, firstname, lastname, othername, email, phoneNumber, passportUrl, password) VALUES (%(nationalId)s , %(firstname)s, %(lastname)s, %(othername)s, %(email)s, %(phoneNumber)s, %(passportUrl)s, %(password)s) RETURNING email"""     
        cur.execute(query, new_user)
        userId = cur.fetchone()[0]
        con.commit()
        con.close

        token = BaseModel.auth_token_encoder(userId)


        registered_user = {
            'userId' : userId,
            'nationalId' : nationalId,
            'firstname' : firstname,
            'lastname' : lastname,
            'othername' : othername,
            'email' : email,
            'phoneNumber' : phoneNumber,
            'passportUrl' : passportUrl
        }

        return [201, token, registered_user]

    def user_sign_in(data):
        user_email = data['email'].strip()
        user_password = data['password'].strip()
        token = ''

        con = database_config.init_test_db()
        cur = con.cursor()
        query = "SELECT userId, email, password FROM users;"
        cur.execute(query)
        data = cur.fetchall()
        res = []

        for i, items in enumerate(data):
            userId, email, password = items
            details = {
                'userId' : userId,
                'email' : email,
                'password' : password 
            }
            res.append(details)

        for detail in res:
            if user_email == detail['email'] and user_password == detail['password']:
                token = BaseModel.auth_token_encoder(detail['email'])
                data = {
                    'userId' : detail['userId'],
                    'email' : detail['email']
                }

                return [200, token, data]
        return [401, 'Please enter the correct email or password']
        
class PartyModel:
    '''Adds all functions that perfom CRUD operations on parties'''
    #List to store all parties
    parties_db = []

    def create_party(data):
        '''Method for creating new party'''

        #Initializes all the required fields for party object
        name = data['name'].strip()
        hqAddress = data['hqAddress'].strip()
        logoUrl = data['logoUrl'].strip()
        id = len(PartyModel.parties_db) + 1

        #Validates that all fields are filled and that none of them are left empty
        if not name:
            return [400 ,'name cannot be empty']
        elif not hqAddress:
            return [400 ,'hqAddress cannot be empty']
        elif not logoUrl:
            return [400, 'logoUrl cannot be empty']
        
        #iterates through party to check that the name provided is unique.
        for party in PartyModel.parties_db:
            if party['name'] == name:
                return [400, 'A party with that name already exists']
        
        #creates a new party filled with all required data.
        new_party = {
            'id' : id,
            'name' : name,
            'hqAddress' : hqAddress,
            'logoUrl' : logoUrl 
        }
    
        #adds new_party to parties_db
        PartyModel.parties_db.append(new_party)

        return [201, new_party]

    def get_all_parties():
        '''Method for getting all parties'''

        #validates that parties_db is not empty
        if len(PartyModel.parties_db) <= 0:
            return [404, 'No Parties to be shown']
        else:
            return [200, PartyModel.parties_db]

    def get_specific_party(party_id):
        '''Method for getting a specific party'''

        #iterates through parties_db to find matching party 
        for party in PartyModel.parties_db:
            if party['id'] == party_id:
                return [200, party]

        return [ 404, 'Party does not exist']
    
    def edit_a_party(party_id, data):
        '''Method for editing a specific party'''

        name = data['name'].strip()

        #Validates that name is not empty
        if not name:
            return [404, 'name cannot be empty']

        #Validates that the name provided does not already exist
        for party in PartyModel.parties_db:
            if party['name'] == name:
                return [400, 'name already exists']

        for party in PartyModel.parties_db:
            if party['id'] == party_id:
                party['name'] = name
                return [200, party]

        return [404, 'party not found']

    def delete_specific_party(party_id):
        '''Method for deleting a specific party'''

        #loops through parties_db to find matching party id
        for party in PartyModel.parties_db:
            if party['id'] == party_id:
                index = party_id - 1
                PartyModel.parties_db.pop(index)
                return [200, 'Party has been succefully deleted']
        
        return [404, 'party not found']

        
class OfficeModel:
    '''Adds all methods that perfom CRUD operations on offices'''

    #List to store all offices
    offices_db = []

    #list that stores all valids values of type
    office_types = ['Federal', 'Legislative', 'State', 'Local Government']

    def create_office(data):
        '''Method to create a new office'''

        name = data['name'].strip()
        type = data ['type'].strip()

        # validates all inputs so that no field is left empty
        if not name:
            return [400 ,'name cannot be empty']
        elif not type:
            return [400, 'type cannot be empty']
        elif type not in OfficeModel.office_types:
            return [400, 'type must be either: Federal, Legislative, State or Local Government']

        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('offices', 'officeName', name) == True:
            return [409, 'Office name already exists']

        new_office = {
            'officeName' : name,
            'officeType' : type
        }

        query = """ INSERT INTO offices (officeName, officeType) VALUES (%(officeName)s, %(officeType)s) RETURNING officeId"""
        cur.execute(query, new_office)
        officeId = cur.fetchone()[0]
        con.commit()
        con.close


        created_office = {
            "officeId" : officeId,
            "officeName" : name,
            "officeType" : type
        }

        return [201, created_office]

    def get_all_offices():
        '''Method to display all offices'''

        #checks if offices_db is empty
        if len(OfficeModel.offices_db) <= 0:
            return [404, 'No Offices to be showed']
        else:
            return [200, OfficeModel.offices_db]

    def get_specific_office(office_id):
        '''Method for getting a specific office'''
        
        #loops through all offices to find one with matching id
        for office in OfficeModel.offices_db:
            if office['id'] == office_id:
                return [200, office]

        return [ 404, 'office does not exist']

    def edit_specific_office(office_id, data):
        ''' Method for editing a specific office'''

        name = data['name'].strip()
        #validates that input provided is not empty
        if not name:
            return [404, 'name cannot be empty']

        #Loops through all offices to find if the name provided already exists
        for office in OfficeModel.offices_db:
            if office['name'] == name:
                return [400, 'name already exists']
        
        #Iterates through all offices to find matching office
        for office in OfficeModel.offices_db:
            if office['id'] == office_id:
                office['name'] = name
                return [200, office]

        return [404, 'office not found']

    def delete_specific_office(office_id):
        '''Method for deleting a specific office'''
        
        #loops through all offices to find matching office
        for office in OfficeModel.offices_db:
            if office['id'] == office_id:
                index = office_id - 1
                OfficeModel.offices_db.pop(index)
                return [200, 'Office has been succefully deleted']
        
        return [404, 'office not found']
