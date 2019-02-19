''' Creates application and sets relevant configuration environment'''

# Third-party imports

from flask import Flask
import os

# Local imports
from app.config import app_config

def create_app(config_name):
    #creates an instance of Flask called app. 
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

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