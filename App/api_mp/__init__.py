from flask import Blueprint

api_mp = Blueprint('api_mp', __name__, static_folder='../static', url_prefix='/mp')

from . import users
