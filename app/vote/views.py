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