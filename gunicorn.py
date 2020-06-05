import multiprocessing

from manager import MODEL
from settings import config_map

config_class = config_map.get(MODEL)
bind = f'{config_class.SERVER_HOST}:{config_class.PORT}'

# 进程的数量，缺省为1
workers = multiprocessing.cpu_count() * 2 + 1

# 设置守护进程（后台运行）, 若将进程交给 supervisor 管理，则必须关闭守护进程
daemon = 'false'

# worker进程的工作方式
# 有 sync, eventlet, gevent, tornado, gthread, 缺省值sync
worker_class = "eventlet"

# 指定项目的根目录，在 apis 加载之前，进入到此目录
chdir = '/usr/src/flaskServer'

# 设置进程文件目录
pidfile = '/usr/src/flaskServer/gunicorn.pid'

# 客户端最大同时连接数，只适用于eventlet， gevent工作方式
worker_connections = 1000

# 设置访问日志和错误信息日志路径
accesslog = '/usr/src/flaskServer/gunicorn_acess.log'
errorlog = '/usr/src/flaskServer/gunicorn_error.log'

# 设置日志等级
loglevel = 'debug'
