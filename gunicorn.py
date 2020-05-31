import multiprocessing

# 监听地址和端口
bind = '127.0.0.1:8000'

# 进程的数量，缺省为1
workers = multiprocessing.cpu_count() * 2 + 1

# 设置守护进程（后台运行）, 若将进程交给 supervisor 管理，则必须关闭守护进程
daemon = 'false'

# worker进程的工作方式
# 有 sync, eventlet, gevent, tornado, gthread, 缺省值sync
worker_class = "gevent"

# 指定项目的根目录，在 apis 加载之前，进入到此目录
chdir = '/home/project/flask-server'

# 设置进程文件目录
pidfile = '/home/project/flask-server/gunicorn.pid'

# 客户端最大同时连接数。只适用于eventlet， gevent工作方式
worker_connections = 1000

# 设置访问日志和错误信息日志路径
accesslog = '/home/project/flask-server/gunicorn_acess.log'
errorlog = '/home/project/flask-server/gunicorn_error.log'

# 设置日志等级
loglevel = 'warning'
