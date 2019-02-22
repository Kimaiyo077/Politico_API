# third party and local imports 
from flask import jsonify, make_response, request
from app.models import OfficeModel, BaseModel
from app.office import office
from flask_jwt_extended import jwt_required, get_jwt_identity



@office.route('/offices', methods=['GET'])
@jwt_required
def get_all_offices():
    response = OfficeModel.get_all_offices()
    message = BaseModel.create_response(response)

    return message


@office.route('/offices', methods=['POST'])
@jwt_required
def add_office():
    data = request.get_json()
    current_user = get_jwt_identity()
    response = OfficeModel.create_office(data, current_user)

    message = BaseModel.create_response(response)
    return message

@office.route('/offices/<office_id>', methods=['GET'])
@jwt_required
def get_a_specific_office(office_id):
    response = OfficeModel.get_specific_office(int(office_id))

    message = BaseModel.create_response(response)
    return message

@office.route('/offices/<office_id>/candidates', methods=['GET'])
@jwt_required
def get_candidates(office_id):
    response = OfficeModel.get_candidates(int(office_id))

    message = BaseModel.create_response(response)
    return message

@office.route('/offices/<office_id>', methods=['PATCH'])
@jwt_required
def edit_a_specific_office(office_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    response = OfficeModel.edit_specific_office(int(office_id), data, current_user)

    message = BaseModel.create_response(response)
    return message

@office.route('/offices/<office_id>', methods=['DELETE'])
@jwt_required
def delete_a_office(office_id):
    current_user = get_jwt_identity()
    response = OfficeModel.delete_specific_office(int(office_id), current_user)

    message = BaseModel.create_response(response)
    return message

@office.route('/offices/<office_id>/register', methods=['POST'])
@jwt_required
def add_candidate(office_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    response = OfficeModel.register_candidate(office_id, data, current_user)

    message = BaseModel.create_response(response)
    return message

@office.route('/offices/<office_id>/results', methods=['GET'])
@jwt_required
def print_results(office_id):
    response = OfficeModel.count_votes(office_id)

    message = BaseModel.create_response(response)
    return message

