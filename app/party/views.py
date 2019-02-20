# Third party and local imports
from flask import jsonify, make_response, request
from app.models import PartyModel, BaseModel
from app.party import party
from flask_jwt_extended import jwt_required, get_jwt_identity


@party.route('/parties', methods=['GET'])
@jwt_required
def get_parties():
    res = PartyModel.get_all_parties()

    message = BaseModel.create_response(res)
    return message

@party.route('/parties', methods=['POST'])
@jwt_required
def add_party():
    current_user = get_jwt_identity()
    data = request.get_json()
    res = PartyModel.create_party(data, current_user)

    message = BaseModel.create_response(res)
    return message

@party.route('/parties/<party_id>', methods=['GET'])
@jwt_required
def get_a_party(party_id):
    res = PartyModel.get_specific_party(int(party_id))

    message = BaseModel.create_response(res)
    return message

@party.route('/parties/<party_id>/name', methods=['PATCH'])
@jwt_required
def edit_a_party(party_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    res = PartyModel.edit_a_party(int(party_id), data, current_user)

    message = BaseModel.create_response(res)
    return message

@party.route('/parties/<party_id>', methods=['DELETE'])
@jwt_required
def delete_a_party(party_id):
    current_user = get_jwt_identity()
    res = PartyModel.delete_specific_party(int(party_id), current_user)

    message = BaseModel.create_response(res)
    return message