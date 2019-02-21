from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from app.models import voteModel
from app.vote import vote
from app.models import BaseModel


@vote.route('/votes', methods=["POST"])
@jwt_required
def cast_vote():
    data = request.get_json()

    response = voteModel.create_vote(data)
    
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