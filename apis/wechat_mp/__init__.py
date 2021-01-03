from flask import Blueprint

api_mp = Blueprint('wechat_mp', __name__, url_prefix='/wechat_mp')

from . import users
