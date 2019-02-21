# Third party and local imports
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity

#Local Imports
from app.models import PartyModel, BaseModel
from app.party import party



@party.route('/parties', methods=['GET'])
@jwt_required
def get_parties():
    '''Handles all requests for getting all parties'''
    res = PartyModel.get_all_parties()

    message = BaseModel.create_response(res)
    return message

@party.route('/parties', methods=['POST'])
@jwt_required
def add_party():
    '''Handles all requests by admin for creating all parties'''
    current_user = get_jwt_identity()
    data = request.get_json()
    res = PartyModel.create_party(data, current_user)

    message = BaseModel.create_response(res)
    return message

@party.route('/parties/<party_id>', methods=['GET'])
@jwt_required
def get_a_party(party_id):
    '''Handles all requests for getting a specific party'''
    res = PartyModel.get_specific_party(int(party_id))

    message = BaseModel.create_response(res)
    return message

@party.route('/parties/<party_id>/name', methods=['PATCH'])
@jwt_required
def edit_a_party(party_id):
    '''Handles all requests for editting a specific party'''
    data = request.get_json()
    current_user = get_jwt_identity()
    res = PartyModel.edit_a_party(int(party_id), data, current_user)

    message = BaseModel.create_response(res)
    return message

@party.route('/parties/<party_id>', methods=['DELETE'])
@jwt_required
def delete_a_party(party_id):
    '''Handles all requests by admin to delete a specific party'''
    current_user = get_jwt_identity()
    res = PartyModel.delete_specific_party(int(party_id), current_user)

    message = BaseModel.create_response(res)
    return message