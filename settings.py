import os
import sys
import redis

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'Server_Flask'))

SECRET_KEY = 'flask_server'
ADMIN_NAME = 'MincoX'
ADMIN_PASSWORD = 'mincoroot'
UPLOAD_FOLDER = 'App/static/upload/'


class MiniProgram:
    AppId = "wx292c8e757abcef11"
    AppSec = "70640820ff52408b0d4707d6bd8a2d95"


class WeChat:
    AppId = ""
    AppSec = ""


class Config:
    DEBUG = True
    HOST = '49.232.19.51'
    PORT = 80

    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PWD = 'root'
    DATABASE = 'MpWeChat'

    SECRET_KEY = 'flask_server'

    # Redis
    REDIS_HOST = '49.232.19.51'
    REDIS_PORT = 63791
    REDIS_PWD = ''

    # flask_session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对 cookie 中的 session_id 进行签名处理
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # session 有效期为: 一周; 单位秒


class Develop(Config):
    """
    开发模式的配置信息
    """
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 80


class Product(Config):
    """
    生产环境配置信息
    """
    DEBUG = False
    HOST = '49.232.19.51'
    PORT = 80


config_map = {
    'develop': Develop,
    'product': Product
}
