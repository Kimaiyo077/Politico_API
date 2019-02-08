#imports Blueprint from flask
from flask import Blueprint

#create a new instance of Blueprint called office
office = Blueprint('office', __name__)

from . import views