''' Creates application and sets relevant configuration environment'''

# Third-party imports

from flask import Flask
import os

# Local imports
from app.config import app_config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Register blueprints


    return app