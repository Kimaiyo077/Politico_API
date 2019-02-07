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