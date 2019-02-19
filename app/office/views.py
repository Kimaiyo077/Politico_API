# third party and local imports 
from flask import jsonify, make_response, request
from app.models import OfficeModel
from app.office import office


@office.route('/offices', methods=['GET'])
def get_all_offices():
    response = OfficeModel.get_all_offices()

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



@office.route('/offices', methods=['POST'])
def add_office():
    data = request.get_json()
    response = OfficeModel.create_office(data)

    if response[0] == 201:
        return make_response(jsonify({
            'status' : response[0],
            'data' : response[1]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])

@office.route('/offices/<office_id>', methods=['GET'])
def get_a_specific_office(office_id):
    response = OfficeModel.get_specific_office(int(office_id))

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
  
@office.route('/offices/<office_id>', methods=['PATCH'])
def edit_a_specific_office(office_id):
    data = request.get_json()
    response = OfficeModel.edit_specific_office(int(office_id), data)

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

@office.route('/offices/<office_id>', methods=['DELETE'])
def delete_a_office(office_id):
    response = OfficeModel.delete_specific_office(int(office_id))

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

@office.route('/offices/<office_id>/register', methods=['POST'])
def add_candidate(office_id):
    data = request.get_json()

    response = OfficeModel.register_candidate(office_id, data)

    if response[0] == 201:
        return make_response(jsonify({
            'status' : response[0],
            'message' : response[1]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])


