from flask import jsonify, make_response
from app.models import PartyModel
from app.party import party


@party.route('/parties', methods=['GET'])
def get_parties():
    if len(PartyModel.parties_db) <= 0:
        return make_response(jsonify({
            'status': 'Not Found',
            'message': 'No parties to show'
        }), 404)
    else:
        return make_response(jsonify({
            'status':'OK',
            'parties': parties_db
        }), 200)