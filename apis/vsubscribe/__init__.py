from flask import Blueprint

api_vsubscribe = Blueprint('vsubscribe', __name__, url_prefix='/vsubscribe')

from . import users
