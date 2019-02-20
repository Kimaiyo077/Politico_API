''' Creates application and sets relevant configuration environment'''

# Third-party imports

from flask import Flask
import os
from flask_jwt_extended import JWTManager

# Local imports
from app.config import app_config

def create_app(config_name):
    #creates an instance of Flask called app. 
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    JWT=JWTManager(app) 

    from app import models
    
    # Register blueprints
    from app.party import party
    app.register_blueprint(party, url_prefix='/api/v1')
    from app.office import office
    app.register_blueprint(office, url_prefix='/api/v1')
    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/api/v2')
    from app.vote import vote
    app.register_blueprint(vote, url_prefix='/api/v2')
    
    return app