# Third party and local imports
from flask import jsonify, make_response, request
from app.models import PartyModel
from app.party import party


@party.route('/parties', methods=['GET'])
def get_parties():
    response = PartyModel.get_all_parties()

    if response[0] == 200:
        return make_response(jsonify({
            'status' : response[0],
            'data' : response[1]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])

@party.route('/parties', methods=['POST'])
def add_party():
    data = request.get_json()

    response = PartyModel.create_party(data)

    if response[0] == 201:
        return make_response(jsonify({
            'status' : response[0],
            'data' : response[1]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' :response[0], 
            'error' : response[1]
        }), response[0])

@party.route('/parties/<party_id>', methods=['GET'])
def get_a_party(party_id):
    response = PartyModel.get_specific_party(int(party_id))

    if response[0] == 200:
        return make_response(jsonify({
            'status' : response[0],
            'data' : response[1]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])

@party.route('/parties/<party_id>/name', methods=['PATCH'])
def edit_a_party(party_id):
    data = request.get_json()
    response = PartyModel.edit_a_party(int(party_id), data)

    if response[0] == 200:
        return make_response(jsonify({
            'status' : response[0],
            'data' : response[1]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])

@party.route('/parties/<party_id>', methods=['DELETE'])
def delete_a_party(party_id):
    response = PartyModel.delete_specific_party(int(party_id))

    if response[0] == 200:
        return make_response(jsonify({
            'status' : response[0],
            'message' : response[1]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])