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
    创建 apis 对象
    :return:
    """

    app = Flask(__name__, static_folder='../static')

    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    global login_manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.refresh_view = 'login'

    app.config['JSON_AS_ASCII'] = False

    CORS(app, supports_credentials=True)
    # CSRFProtect(apis)

    global redis_store
    redis_store = redis.StrictRedis(host=config_class.HOST, port=config_class.REDIS_PORT)
    app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 2
    session = Session()
    session.init_app(app)

    # 配置 qq 邮箱
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = '903444601@qq.com'
    app.config['MAIL_PASSWORD'] = 'fchqhwiuotipbbac'

    # 解决循环导入问题
    from apis.wechat_mp import api_mp
    from apis.proxy import api_proxy
    from apis.vmodel import api_vmodel

    app.register_blueprint(api_mp)
    app.register_blueprint(api_proxy)
    app.register_blueprint(api_vmodel)

    return app
