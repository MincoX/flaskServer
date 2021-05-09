from flask import Blueprint

api_common = Blueprint('common', __name__, url_prefix='/common')

from . import user
