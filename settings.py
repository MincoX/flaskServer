import os
import sys
import redis

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'flaskServer'))


class Config:
    SECRET_KEY = 'flask_server'

    DEBUG = True
    SERVER_HOST = '127.0.0.1'
    PORT = 5000

    HOST = '47.102.134.101'

    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PWD = 'mincoroot'
    DATABASE = None

    MQ_PORT = 5672
    MQ_USER = 'root'
    MQ_PWD = 'mincoroot'

    # Redis
    REDIS_PORT = 6379
    REDIS_PWD = None

    # flask_session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对 cookie 中的 session_id 进行签名处理
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # session 有效期为: 一周; 单位秒


class Develop(Config):
    """
    开发模式的配置信息
    """
    DEBUG = True
    SERVER_HOST = '127.0.0.1'
    PORT = 5000


class Product(Config):
    """
    生产环境配置信息
    """
    DEBUG = False
    SERVER_HOST = '0.0.0.0'
    PORT = 5000


config_map = {
    'develop': Develop,
    'product': Product
}
