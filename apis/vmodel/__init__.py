from flask import Blueprint

api_vmodel = Blueprint('vmodel', __name__, url_prefix='/vmodel')

from . import proxy
from . import account
