from flask import jsonify, make_response, request
from app.models import voteModel
from app.vote import vote
from app.models import BaseModel


@vote.route('/votes', methods=["POST"])
def cast_vote():
    data = request.get_json()

    response = voteModel.create_vote(data)
    
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