# Third party and local imports
from flask import jsonify, make_response, request
from app.models import PartyModel
from app.party import party
from flask_jwt_extended import jwt_required, get_jwt_identity


def response_message(response):
    if response[0] == 201 or response[0] == 200:
        return make_response(jsonify({
            'status' : response[0],
            'token' : response[1],
            'User' : response[2]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])


@party.route('/parties', methods=['GET'])
@jwt_required
def get_parties():
    response = PartyModel.get_all_parties()
    message = response_message(response)

    return message

@party.route('/parties', methods=['POST'])
@jwt_required
def add_party():
    data = request.get_json()
    current_user = get_jwt_identity()
    response = PartyModel.create_party(data, current_user)
    message = response_message(response)

    return message

@party.route('/parties/<party_id>', methods=['GET'])
@jwt_required
def get_a_party(party_id):
    response = PartyModel.get_specific_party(int(party_id))
    message = response_message(response)

    return message

@party.route('/parties/<party_id>/name', methods=['PATCH'])
@jwt_required
def edit_a_party(party_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    response = PartyModel.edit_a_party(int(party_id), data, current_user)
    message = response_message(response)

    return message

@party.route('/parties/<party_id>', methods=['DELETE'])
@jwt_required
def delete_a_party(party_id):
    current_user = get_jwt_identity()
    response = PartyModel.delete_specific_party(int(party_id), current_user)
    message = response_message(response)

    return message