from flask import Blueprint

api_mp = Blueprint('mp', __name__, url_prefix='/mp')

from . import users
