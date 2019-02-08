#imports Blueprint from flask.
from flask import Blueprint

#creates an instance of blueprint called flask.
party = Blueprint('party', __name__)

from . import views