from flask import Blueprint

api_proxy = Blueprint('proxy', __name__, url_prefix='/proxy')

from . import proxy
