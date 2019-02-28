from flask import make_response, request, jsonify
from app.models import userModel
from app.auth import auth


def response_message(response):
    if response[0] == 201 or response[0] == 200:
        return make_response(jsonify({
            'status' : response[0],
            'token' : response[1],
            'User' : response[2]
        }), response[0])
    else:
        return make_response(jsonify({
            'status' : response[0],
            'error' : response[1]
        }), response[0])


@auth.route('/auth/signup', methods=['POST'])
def register_user():
    data = request.get_json(force=True)
    resp = userModel.create_account(data)

    message = response_message(resp)
    return message

@auth.route('/auth/login', methods=['POST'])
def user_login():
    data = request.get_json()
    resp = userModel.user_sign_in(data)

    message = response_message(resp)
    return message
