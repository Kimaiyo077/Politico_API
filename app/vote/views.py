#Third party imports
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required

#Local imports
from app.models import voteModel
from app.vote import vote
from app.models import BaseModel


@vote.route('/votes', methods=["POST"])
@jwt_required
def cast_vote():
    '''Endpoint for allowing users to cast votes'''

    data = request.get_json()

    response = voteModel.create_vote(data)
    
    message = BaseModel.create_response(response)

    return message

@vote.route('/votes/<user_id>', methods=["GET"])
@jwt_required
def get_specific_vote(user_id):
    response = voteModel.get_user_votes(user_id)

    message = BaseModel.create_response(response)

    return message