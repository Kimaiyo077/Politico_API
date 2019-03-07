# Third party imports
import psycopg2
import datetime
import os
import re
from flask_jwt_extended import create_access_token
from flask import make_response, jsonify

#Local imports
from app import database_config
from app.validations import validations

class BaseModel:
    ''' Base class that holds methods that needs to be reused by other classes'''

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

    def check_if_admin(value):

        isadmin = value['role']

        if isadmin:
            return True
        else:
            return False
            
    def check_if_not_null(data):

        for i in data:
            if not data[i]:
                return [400, "{} cannot be empty".format(i)]

        return None

    def create_response(response):
        if response[0] == 201 or response[0] == 200:
            return make_response(jsonify({
                'status' : response[0],
                'data' : response[1],
            }), response[0])
        else:
            return make_response(jsonify({
                'status' : response[0],
                'error' : response[1]
            }), response[0])

    def get_name(name, table_name, field_name, value):
        con = database_config.init_test_db()
        cur = con.cursor()
        query = """SELECT {} FROM {} WHERE {}='{}';""".format(name, table_name, field_name, value)
        cur.execute(query)
        res = cur.fetchall()[0][0]

        return res


class userModel(BaseModel):
    '''Class that handles user sign in and sign up requests'''
    
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
        elif BaseModel.check_if_exists('users', 'phoneNumber', phoneNumber) == True:
            return [409, 'That phone number is in use already']
        elif BaseModel.check_if_exists('users', 'passportUrl', passportUrl) == True:
            return [409, 'That passport URL is in use already']

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

        query = """ INSERT INTO users (nationalId, firstname, lastname, othername, email, phoneNumber, passportUrl, password) VALUES (%(nationalId)s , %(firstname)s, %(lastname)s, %(othername)s, %(email)s, %(phoneNumber)s, %(passportUrl)s, %(password)s) RETURNING userId"""     
        cur.execute(query, new_user)
        userId = cur.fetchone()[0]
        con.commit()

        query = """SELECT isadmin FROM users WHERE email ='{}';""".format(email)
        cur.execute(query)
        isadmin = cur.fetchall()[0][0]
        
        con.close

        token = create_access_token(identity={'email': email, 'role' : isadmin})


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
        query = "SELECT userId, nationalId, firstname, lastname, email, password, isadmin FROM users;"
        cur.execute(query)
        data = cur.fetchall()
        res = []

        for i, items in enumerate(data):
            userId, nationalId, firstname, lastname, email, password, isadmin = items
            details = {
                'userId' : userId,
                'nationalId' : int(nationalId),
                'firstname' : firstname,
                'lastname' : lastname,
                'email' : email,
                'password' : password,
                'isadmin' : isadmin
            }
            res.append(details)

        for detail in res:
            if user_email == detail['email'] and user_password == detail['password']:
                token = create_access_token(identity={'email':detail['email'], 'role': detail['isadmin']})
                data = {
                    'userId' : detail['userId'],
                    'nationalId' : detail['nationalId'],
                    'firstname' : detail['firstname'],
                    'lastname' : detail['lastname'],
                    'email' : detail['email']
                }

                return [200, token, data]
        return [401, 'Please enter the correct email or password']
        
class PartyModel:
    '''Adds all functions that perfom CRUD operations on parties'''

    def create_party(data, current_user):
        '''Method for creating new party'''

        #Initializes all the required fields for party object
        name = data['name'].strip()
        hqAddress = data['hqAddress'].strip()
        logoUrl = data['logoUrl']

        new_party = {
            'partyName' : name,
            'hqAddress' : hqAddress,
            'logoUrl' : logoUrl
        }

        #Validates that all fields are filled and that none of them are left empty
        valid = BaseModel.check_if_not_null(new_party)

        if valid != None:
            return valid

        if not validations.validate_url(logoUrl):
            return [400, 'logo URL is not a valid url']
        
        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('parties', 'partyName', name) == True:
            return [409, 'Party already exists']
        
        if BaseModel.check_if_admin(current_user) == False:
            return [401, 'Nice try, But you are not authorized']


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
    
    def edit_a_party(party_id, data, current_user):
        '''Method for editing a specific party'''

        name = data['name'].strip()

        #Validates that name is not empty
        if not name:
            return [404, 'name cannot be empty']

        if BaseModel.check_if_exists('parties', 'partyName', name) == True:
            return [409, "Party already exists"]

        if BaseModel.check_if_exists('parties', 'partyId', party_id) == False:
            return [404, "Party doesn't exist"]
        
        if BaseModel.check_if_admin(current_user) == False:
            return [401, 'Nice try, But you are not authorized']

        con = database_config.init_test_db()
        cur = con.cursor()

        query = """UPDATE parties SET partyName = '{}' WHERE partyId = {};""".format(name, party_id)

        cur.execute(query)

        con.commit()
        con.close()

        return [200, "Changes made successfully"]

    def delete_specific_party(party_id, current_user):
        '''Method for deleting a specific party'''

        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('parties', 'partyId', party_id) == False:
            return [404, "Party cannot be found"]

        if BaseModel.check_if_admin(current_user) == False:
            return [401, 'You are not authorized']

        query = " DELETE FROM parties WHERE partyId = {}".format(party_id)

        cur.execute(query)

        con.commit()
        con.close()

        return [200, "Party successfully deleted"]

        
class OfficeModel:
    '''Adds all methods that perfom CRUD operations on offices'''

    #list that stores all valids values of type
    office_types = ['Federal', 'Legislative', 'State', 'Local Government']

    def create_office(data, current_user):
        '''Method to create a new office'''

        name = data['name'].strip()
        type = data ['type'].strip()

        new_office = {
            'officeName' : name,
            'officeType' : type
        }


        # validates all inputs so that no field is left empty
        valid = BaseModel.check_if_not_null(new_office)

        if valid != None:
            return valid

        if type not in OfficeModel.office_types:
            return [400, 'type must be either: Federal, Legislative, State or Local Government']

        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('offices', 'officeName', name) == True:
            return [409, 'Office name already exists']

        if BaseModel.check_if_admin(current_user) == False:
            return [401, 'Nice try, But you are not authorized']

       
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

    def edit_specific_office(office_id, data, current_user):
        ''' Method for editing a specific office'''

        if BaseModel.check_if_admin(current_user) == False:
            return [401, 'Nice try, But you are not authorized']
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

    def delete_specific_office(office_id, current_user):
        '''Method for deleting a specific office'''
        
        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('offices', 'officeId', office_id) == False:
            return [404, 'Office not found']

        if BaseModel.check_if_admin(current_user) == False:
            return [401, 'Nice try, But you are not authorized']

        query = " DELETE FROM offices WHERE officeId = {}".format(office_id)

        cur.execute(query)

        con.commit()
        con.close()

        return [200, "Office successfully deleted"]
    
    def register_candidate(office_id, data, current_user):
        '''Method for adding a candidate'''
        id = data['user_id']
        party = data['party_id']

        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('offices', 'officeId', office_id) == False:
            return [404, 'Office does not exist']
        
        if BaseModel.check_if_exists('parties', 'partyId', party) == False:
            return [404, 'Party does not exist']

        if BaseModel.check_if_exists('users', 'userId', id) == False:
            return [404, 'User does not exist']


        office_name = BaseModel.get_name('officeName','offices', 'officeId', office_id)
        party_name = BaseModel.get_name('partyName','parties', 'partyId', party)
        user_first_name = BaseModel.get_name('firstname','users', 'userId', id)
        user_last_name = BaseModel.get_name('lastname', 'users', 'userId', id)

        new_candidate = {
            'partyId' : party,
            'officeId' : office_id,
            'userId' : id
        }
        query = """INSERT INTO candidates (partyId, officeId, userId) VALUES (%(partyId)s,%(officeId)s, %(userId)s) RETURNING candidateId"""

        cur.execute(query, new_candidate)
        candidate_id = cur.fetchall()[0]
        con.commit()
        con.close


        res = {
            'CandidateId' : candidate_id,
            'Office Name' : office_name,
            'Candidate Name' : user_first_name,
            'Party Name' : party_name
        }

        return [201, res]

    def get_candidates(office_id):
        con = database_config.init_test_db()
        cur = con.cursor()

        if BaseModel.check_if_exists('candidates', 'officeId', office_id) == False:
            return [404, "No candidates exist for the office"]

        query = """SELECT candidateId, partyId, userId FROM candidates WHERE officeId = '{}';""".format(office_id)
        cur.execute(query)
        data = cur.fetchall()

        candidates = []

        for i, items in enumerate(data):
            candidateId, partyId, userId = items
            partyName = BaseModel.get_name('partyName','parties', 'partyId', partyId)
            candidate_first_name = BaseModel.get_name('firstname','users', 'userId', userId)
            candidate_last_name = BaseModel.get_name('lastname','users', 'userId', userId)
            officeName = BaseModel.get_name('officeName','offices', 'officeId', office_id)

            candidate = {
                "candidateId" : candidateId,
                "candidate Name" : candidate_first_name + " " + candidate_last_name,
                "Party" : partyName,
                "office Name" : officeName 
            }

            candidates.append(candidate)

        if len(candidates) <= 0:
            return [400, "This office has no candidate running for the seat."]


        return [200, candidates]

    def count_votes(office_id):
        counted_votes = []
        candidates = set()

        con = database_config.init_test_db()
        cur = con.cursor()

        query = """SELECT * FROM votes WHERE officeId = '{}'""".format(office_id)

        cur.execute(query)
        votes = cur.fetchall()

        for vote in votes:
            candidates.add(vote[2])

        for candidate in candidates:
            results = 0
            for vote in votes:
                if vote[2] == candidate:
                    results += 1

            office_name = BaseModel.get_name('officeName', 'offices', 'officeId', office_id)
            user_id = BaseModel.get_name('userId','candidates', 'candidateId', candidate)
            user_first_name = BaseModel.get_name('firstname','users', 'userId', user_id)
            user_last_name = BaseModel.get_name('lastname','users', 'userId', user_id) 

            counted_votes.append({"office" : office_name, "candidate" : user_first_name + " " + user_last_name, "result" : results})

        con.commit()
        con.close()

        return [200, counted_votes]

class voteModel(BaseModel):
    '''Class that holds all methods handle user voting'''

    def create_vote(data):

        candidate_id = data['candidate']
        user_id = data['user']

        if BaseModel.check_if_exists('candidates', 'candidateId', candidate_id) == False:
            return [404, 'Candidate does not exist']
        
        query_one = """ SELECT officeId FROM candidates WHERE candidateId = '{}' ;""".format(candidate_id)

        con = database_config.init_test_db()
        cur = con.cursor()

        cur.execute(query_one)
        office_id = cur.fetchone()

        new_vote = {
            "officeId" : office_id,
            "candidateId" : candidate_id,
            "userId" : user_id
        }

        query_two = """INSERT INTO votes (officeId, candidate, createdBy) VALUES (%(officeId)s,%(candidateId)s,%(userId)s);"""

        try:
            cur.execute(query_two, new_vote)
        except:
            return [400, 'You have already voted']

        id = BaseModel.get_name('userId','candidates', 'candidateId', candidate_id)


        candidate_first_name = BaseModel.get_name('firstname','users', 'userId',id)
        candidate_last_name = BaseModel.get_name('lastname','users', 'userId', id)
        office_name = BaseModel.get_name('officeName','offices', 'officeId', office_id[0])
        user_first_name = BaseModel.get_name('firstname','users', 'userId', user_id)
        user_last_name = BaseModel.get_name('lastname','users', 'userId', user_id)

        con.commit()
        con.close()

        
        vote = {
            "candidate": candidate_first_name + " " + candidate_last_name,
            "office" : office_name,
            "created by" : user_first_name + " " + user_last_name 
        }

        return [201, vote]

    def get_user_votes(user_id):

        votes = []

        con = database_config.init_test_db()
        cur = con.cursor()

        query = """SELECT * FROM votes WHERE createdBy = '{}';""".format(user_id)

        cur.execute(query)
        data = cur.fetchall()

        
        for i, items in enumerate(data):
            vote_id, officeId, candidate, createdOn, createdBy = items

            office_name = BaseModel.get_name('officeName','offices', 'officeId', officeId)
            candidate_first_name = BaseModel.get_name('firstname','users', 'userId', candidate)
            candidate_last_name = BaseModel.get_name('lastname','users', 'userId', candidate)

            vote = {
                "office" : office_name,
                "candidate" : candidate_first_name + " " + candidate_last_name,
                "createdOn" : createdOn,
            }
            votes.append(vote)

        if len(votes) <= 0:
            return [404, "You have not voted yet."]

        return [200, votes]