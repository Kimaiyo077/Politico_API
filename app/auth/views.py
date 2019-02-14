from flask import make_response, request, jsonify
from app.models import userModel
from app.auth import auth

@auth.route('/auth/signup', methods=['POST'])
def register_user():
    data = request.get_json()
    response = userModel.create_account(data)

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