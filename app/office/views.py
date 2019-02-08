# third party and local imports 
from flask import jsonify, make_response, request
from app.models import OfficeModel
from app.office import office


@office.route('/offices', methods=['GET'])
def get_all_offices():
    # checks that offices_db is not empty and returns error if so.
    if len(OfficeModel.offices_db) <= 0:
        return make_response(jsonify({
            'status': 404,
            'error' : 'No Offices to be showed'
        }), 404)
    else:
        return make_response(jsonify({
            'status' : 200,
            'offices' : OfficeModel.offices_db
        }), 200)

@office.route('/addoffices', methods=['POST'])
def add_office():
    data = request.get_json()
    name = data['name']
    type = data['type']
    id = len(OfficeModel.offices_db) + 1

    #runs data through validations to ensure that data is present and not missing.
    if not name:
        return make_response(jsonify({
            'status': 400,
            'error': 'Name cannot be empty'
        }), 400)
    elif not type:
        return make_response(jsonify({
            'status': 400,
            'error': 'type cannot be empty'
        }), 400)

    #ensure name is alphabetical with no spaces
    if not name.isalpha():
        return make_response(jsonify({
            'status': 400,
            'error': 'Name must be alphabetical with no spaces'
        }), 400)

    new_office = {
        'id' : id,
        'name' : name,
        'type' : type
    }
    
    #adds new offices to offices_db
    OfficeModel.offices_db.append(new_office)

    return make_response(jsonify({
        'Status' : 201,
        'Office' : new_office
    }), 201)

@office.route('/offices/<office_id>', methods=['GET'])
def get_a_specific_office(office_id):
    #loops through offices_db to find office with matching id and returns it
    for office in OfficeModel.offices_db:
        if office['id'] == int(office_id):
            return make_response(jsonify({
                'status' : 200,
                'data' : office
            }), 200)

    return make_response(jsonify({
        'status': 404,
        'error': 'office does not exist'
    }), 404)


@office.route('/offices/<office_id>', methods=['PATCH'])
def edit_a_specific_office(office_id):
    data = request.get_json()
    name = data['name']

    #validates that new name is only alphabetical letters with no spaces
    if not name.isalpha():
        return make_response(jsonify({
            'status': 400,
            'error': 'Name must be alphabetical with no spaces'
        }), 400)

    #loops through all offices in office_db to find matching id and replaces name with new name.
    for office in OfficeModel.offices_db:
        if office['id'] == int(office_id):
            office['name'] = name
            return make_response(jsonify({
                'status' : 200,
                'data' : office
                }), 200)

    return make_response(jsonify({
        'status' : 404,
        'error' : 'Office Not Found'
    }), 404)

@office.route('/office/<office_id>', methods=['DELETE'])
def delete_a_office(office_id):
    # loops through offices_db to find matching office and the removes it from offices db.
    for office in OfficeModel.offices_db:
        if office['id'] == int(office_id):
            index = int(office_id) - 1
            OfficeModel.offices_db.pop(index)
            return make_response(jsonify({
                'status' : 200,
                'message' : 'Office has been deleted successfuly'
            }), 200)

    return make_response(jsonify({
        'status' : 404,
        'error' : 'Office not found.'
    }))