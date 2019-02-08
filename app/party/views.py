# Third party and local imports
from flask import jsonify, make_response, request
from app.models import PartyModel
from app.party import party


@party.route('/parties', methods=['GET'])
def get_parties():
    #checks to ensure that there are existing parties to get
    if len(PartyModel.parties_db) <= 0:
        return make_response(jsonify({
            'status': 'Not Found',
            'message': 'No parties to show'
        }), 404)
    else:
        return make_response(jsonify({
            'status':'OK',
            'parties': PartyModel.parties_db
        }), 200)

@party.route('/addparty', methods=['POST'])
def add_party():
    data = request.get_json()
    name = data['name']
    hqAddress = data['hqAddress']
    logoUrl = data['logoUrl']
    id = len(PartyModel.parties_db) + 1

    #Validations to check that correct data is being added to parties_db.
    if not name:
        return make_response(jsonify({
            'status': 400,
            'error': 'Name cannot be empty'
        }), 400)
    elif not hqAddress:
        return make_response(jsonify({
            'status': 400,
            'error': 'HQ address cannot be empty'
        }), 400)
    elif not logoUrl:
        return make_response(jsonify({
            'status': 400,
            'error': 'Logo URLcannot be empty'
        }), 400)

    #checks lengh of name.
    if len(name) > 20:
        return make_response(jsonify({
            'status': 400,
            'error': 'Name cannot be longer than 20 characters'
        }), 400)

    #creates a new party filled with all required data.
    new_party = {
        'id' : id,
        'name' : name,
        'hqAddress' : hqAddress,
        'logoUrl' : logoUrl 
    }
    
    #adds new_party to parties_db
    PartyModel.parties_db.append(new_party)

    return make_response(jsonify({
        'Status' : 'OK',
        'Message' : 'New Party added',
        'Party' : new_party['name']
    }), 201)

@party.route('/parties/<party_id>', methods=['GET'])
def get_a_party(party_id):
    #checks if party is existing in partes_db.
    for party in PartyModel.parties_db:
        if party['id'] == int(party_id):
            return make_response(jsonify({
                'status' : 200,
                'data' : party
            }), 200)

    return make_response(jsonify({
        'status': 404,
        'error': 'Party does not exist'
    }), 404)

@party.route('/parties/<party_id>/name', methods=['PATCH'])
def edit_a_party(party_id):
    data = request.get_json()
    name = data['name']

    #validations to ensure only correct data is used for editing
    if not name:
        return make_response(jsonify({
            'status': 400,
            'error': 'Name cannot be empty'
        }), 400)
    elif len(name) > 20:
        return make_response(jsonify({
            'status': 400,
            'error': 'Name cannot be longer than 20 characters'
        }), 400)

    for party in PartyModel.parties_db:
        if party['id'] == int(party_id):
            party['name'] = name
            return make_response(jsonify({
                'status' : 200,
                'data' : party
                }), 200)

    return make_response(jsonify({
        'status' : 404,
        'error' : 'Party Not Found'
    }), 404)

@party.route('/parties/<party_id>', methods=['DELETE'])
def delete_a_party(party_id):

    #the for loop loops through every party and finds the one matching id in the list 
    for party in PartyModel.parties_db:
        if party['id'] == int(party_id):
            index = int(party_id) - 1
            #the macthing party is removed from the list witj pop() functions.
            PartyModel.parties_db.pop(index)
            return make_response(jsonify({
                'status' : 200,
                'message' : 'Party has been deleted successfuly'
            }), 200)

    return make_response(jsonify({
        'status' : 404,
        'error' : 'Party not found.'
    }))