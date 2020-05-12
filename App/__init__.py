import redis

from flask import Flask
from flask_cors import *
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from settings import config_map

redis_store = None
login_manager = None


def create_app(config_name):
    """
    创建 app 对象
    :return:
    """

    app = Flask(__name__)

    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    global login_manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.refresh_view = 'login'

    app.config['JSON_AS_ASCII'] = False

    CORS(app, supports_credentials=True)
    # CSRFProtect(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 2
    session = Session()
    session.init_app(app)

    # 解决循环导入问题
    from App.api_mp import api_mp
    app.register_blueprint(api_mp)

    return app
