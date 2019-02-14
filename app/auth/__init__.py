from flask import Blueprint

#create a new instance of Blueprint called auth
auth = Blueprint('auth', __name__)

from . import views