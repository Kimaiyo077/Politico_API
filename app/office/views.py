from flask import jsonify, make_response, request
from app.models import OfficeModel
from app.office import office


@office.route('/offices', methods=['GET'])
def get_all_offices():
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

    new_office = {
        'id' : id,
        'name' : name,
        'type' : type
    }
    
    OfficeModel.offices_db.append(new_office)

    return make_response(jsonify({
        'Status' : 201,
        'Office' : new_office
    }), 201)