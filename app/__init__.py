''' Creates application and sets relevant configuration environment'''

# Third-party imports

from flask import Flask, jsonify
import os
import datetime
from flask_jwt_extended import JWTManager

# Local imports
from app.config import app_config

''' All error handlers for the api'''
def pageNotFound(error):
    return jsonify({
        "status": 404,
        "error": "The requested URL was not found on the server. If you entered the URL manually please check if it is the correct url."
    }), 404


def badRequest(error):
    return jsonify({
        "status": 400,
        "error": "Please make sure you have entered valid data"
    }), 400


def methodNotAllowed(error):
    return jsonify({
      "status": 405,
      "error": "The method is not allowed for the requested URL"
    })


def internalServerError(error):
    return jsonify({
      "status": 500,
      "error": "The server is not responding correctly, Try again later"
    })

def create_app(config_name):
    #creates an instance of Flask called app. 
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=60)
    JWT=JWTManager(app) 

    from app import models
    
    # Register blueprints and error handlers
    app.register_error_handler(404, pageNotFound)
    app.register_error_handler(405, methodNotAllowed)
    app.register_error_handler(400, badRequest)
    app.register_error_handler(500, internalServerError)
    from app.party import party
    app.register_blueprint(party, url_prefix='/api/v2')
    from app.office import office
    app.register_blueprint(office, url_prefix='/api/v2')
    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/api/v2')
    from app.vote import vote
    app.register_blueprint(vote, url_prefix='/api/v2')
    
    return app