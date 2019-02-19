import psycopg2
import datetime
import os
import jwt
import re
from functools import wraps
from app import database_config
from app.validations import validations

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
        
    def auth_token_decoder(token):
        try:
            payload = jwt.decode(token, os.getenv('SECRET'))
            return payload['user']

        except jwt.ExpiredSignatureError:
            return [401, 'Token has expired. Please log in again.']

        except jwt.InvalidTokenError:
            return [401, 'Invalid token. Please log in again.']

    def token_required(f):

        @wraps(f)
        def wrapper_function(*args, **kws):
            if not 'Authorization' in request.headers:
               abort(401)

            request.user = None
            secret = os.getenv('SECRET')

            data = request.headers['Authorization'].encode('ascii','ignore')
            token = str.replace(str(data), 'Bearer ','')

            try:
                user = jwt.decode(token, secret, algorithms=['HS256'])['user']
            except:
                abort(401)

            return f(user, *args, **kws)
        
        return wrapper_function


class userModel(BaseModel):
    
    def create_account(data):
        nationalId = data['nationalId'].strip()
        firstname = data['firstname'].strip()
        lastname = data['lastname'].strip()
        othername = data['othername'].strip()
        email = data['email'].strip()
        phoneNumber = data['phoneNumber']
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

        if not validations.validate_email(email):
            return [400, 'invalid email format']
        elif not validations.validate_url(passportUrl):
            return [400, 'invalid url']

        if phoneNumber:
            if not validations.validate_phone_number(phoneNumber):
                return [400, 'Invalid phone number']

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

    def create_party(data):
        '''Method for creating new party'''

        #Initializes all the required fields for party object
        name = data['name'].strip()
        hqAddress = data['hqAddress'].strip()
        logoUrl = data['logoUrl']

        #Validates that all fields are filled and that none of them are left empty
        if not name:
            return [400 ,'name cannot be empty']
        elif not hqAddress:
            return [400 ,'hqAddress cannot be empty']
        elif not logoUrl:
            return [400, 'logoUrl cannot be empty']

        if not validations.validate_url(logoUrl):
            return [400, 'logo URL is not a valid url']
        
        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('parties', 'partyName', name) == True:
            return [409, 'Party name already exists']

        new_party = {
            'partyName' : name,
            'hqAddress' : hqAddress,
            'logoUrl' : logoUrl
        }

        query = """ INSERT INTO parties (partyName, hqAddress, logoUrl) VALUES (%(partyName)s, %(hqAddress)s, %(logoUrl)s) RETURNING partyId"""
        cur.execute(query, new_party)
        partyId = cur.fetchone()[0]
        con.commit()
        con.close


        created_party = {
            "partyId" : partyId,
            "partyName" : name,
            "hqAddress" : hqAddress,
            "logoUrl" : logoUrl
        }

        return [201, created_party]


    def get_all_parties():
        '''Method for getting all parties'''

        con = database_config.init_test_db()
        cur = con.cursor()

        query = """SELECT * FROM parties;"""
        cur.execute(query)

        data = cur.fetchall()

        party_list = []

        for i, items in enumerate(data):
            partyId, partyName, hqAddress, logoUrl = items
            party = {
                "partyId" : partyId,
                "partyName" : partyName,
                "hqAddress" : hqAddress,
                "logoUrl" : logoUrl
            }
            party_list.append(party)

        if len(party_list) <= 0:
            return [404, "No offices to show"]

        return [200, party_list]

    def get_specific_party(party_id):
        '''Method for getting a specific party'''

        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('parties', 'partyId', party_id) == False:
            return [404, "Party not found"]

        query = """SELECT partyId, partyName, hqAddress, logoUrl FROM parties WHERE partyId = {};""".format(party_id)
        cur.execute(query)
        data = cur.fetchall()[0]
        party = {
            "partyid" : data[0],
            "partyName" : data[1],
            "hqAddress" : data[2],
            "logoUrl" : data[3]
        }

        return [200, party]
    
    def edit_a_party(party_id, data):
        '''Method for editing a specific party'''

        name = data['name'].strip()

        #Validates that name is not empty
        if not name:
            return [404, 'name cannot be empty']

        if BaseModel.check_if_exists('parties', 'partyName', name) == True:
            return [409, "Party already exists"]

        if BaseModel.check_if_exists('parties', 'partyId', party_id) == False:
            return [404, "Party doesn't exist"]

        con = database_config.init_test_db()
        cur = con.cursor()

        query = """UPDATE parties SET partyName = '{}' WHERE partyId = {};""".format(name, party_id)

        cur.execute(query)

        con.commit()
        con.close()

        return [200, "Changes made successfully"]

    def delete_specific_party(party_id):
        '''Method for deleting a specific party'''

        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('parties', 'partyId', party_id) == False:
            return [404, "No party with ID:{}".format(party_id)]

        query = " DELETE FROM parties WHERE partyId = {}".format(party_id)

        cur.execute(query)

        con.commit()
        con.close()

        return [200, "Party successfully deleted"]

        
class OfficeModel:
    '''Adds all methods that perfom CRUD operations on offices'''

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

        con = database_config.init_test_db()
        cur = con.cursor()

        query = """SELECT * FROM offices;"""
        cur.execute(query)

        data = cur.fetchall()

        office_list = []

        for i, items in enumerate(data):
            officeId, officeType, officeName = items
            office = {
                "officeId" : officeId,
                "officeName" : officeName,
                "officeType" : officeType
            }
            office_list.append(office)

        if len(office_list) <= 0:
            return [404, "No offices to show"]

        return [200, office_list]

    def get_specific_office(office_id):
        '''Method for getting a specific office'''
        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('offices', 'officeId', office_id) == False:
            return [404, "Office not found"]

        query = """SELECT officeId, officeName, officeType FROM offices WHERE officeId = {};""".format(office_id)
        cur.execute(query)
        data = cur.fetchall()[0]
        office = {
            "officeid" : data[0],
            "officeName" : data[1],
            "officeType" : data[2]
        }

        return [200, office]

    def edit_specific_office(office_id, data):
        ''' Method for editing a specific office'''

        name = data['name'].strip()
        #validates that input provided is not empty
        if not name:
            return [404, 'name cannot be empty']

        
        if BaseModel.check_if_exists('offices', 'officeName', name) == True:
            return [409, "office already exists"]

        if BaseModel.check_if_exists('offices', 'officeId', office_id) == False:
            return [404, "office doesn't exist"]

        con = database_config.init_test_db()
        cur = con.cursor()

        query = """UPDATE offices SET officeName = '{}' WHERE officeId = {};""".format(name, office_id)

        cur.execute(query)

        con.commit()
        con.close()

        return [200, "Changes made successfully"]

    def delete_specific_office(office_id):
        '''Method for deleting a specific office'''
        
        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('offices', 'officeId', office_id) == False:
            return [404, "No office with ID:{}".format(office_id)]

        query = " DELETE FROM offices WHERE officeId = {}".format(office_id)

        cur.execute(query)

        con.commit()
        con.close()

        return [200, "Office successfully deleted"]
    
    def register_candidate(office_id, data):
        '''Method for adding a candidate'''
        id = data['user_id']

        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('offices', 'officeId', office_id) == False:
            return [404, "No office with ID:{}".format(office_id)]

        if BaseModel.check_if_exists('users', 'userId', id) == False:
            return [404, "No user with that ID: {}".format(id)]

        new_candidate = {
            'officeId' : office_id,
            'userId' : id
        }
        query = """INSERT INTO candidates (officeId, userId) VALUES (%(officeId)s, %(userId)s) RETURNING candidateId"""

        cur.execute(query, new_candidate)
        candidate_id = cur.fetchall()[0]
        con.commit()
        con.close


        res = {
            'CandidateId' : candidate_id,
            'Office_id' : office_id,
            'User_id' : id
        }

        return [201, res]

class voteModel(BaseModel):

    def create_vote(data):

        candidate_id = data['candidate']
        user_id = data['user']

        if BaseModel.check_if_exists('candidates', 'candidateId', candidate_id) == False:
            return [404, 'Candidate does not exist']
        
        query_one = """ SELECT officeId FROM candidates WHERE candidateId = '{}' RETURNING officeId;""".format(candidate_id)

        con = database_config.init_test_db()
        cur = con.cursor()

        cur.execute(query_one)
        office_id = cur.fetchone()[0]

        new_vote = {
            "officeId" : office_id,
            "candidateId" : candidate_id,
            "userId" : user_id
        }

        query_two = """INSERT INTO vote (candidate,officeId, createdBy) VALUES \ (%(candidateId)s,%(officeId)s,%(userId)s);"""

        try:
            cur.execute(query_two)
        except:
            return [400, 'You have already voted']

        con.commit()
        con.close()

        vote = {
            "candidate": candidate_id,
            "office" : office_id,
            "created by" : user_id 
        }

        return [201, vote]
