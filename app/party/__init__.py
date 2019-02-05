from flask import Blueprint

party = Blueprint('party', __name__)

from . import views