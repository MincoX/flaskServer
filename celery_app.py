from datetime import timedelta

from celery import Celery
from kombu import Queue, Exchange
from celery.schedules import crontab

import settings

c_app = Celery(
    broker=f'amqp://{settings.Product.MQ_USER}:{settings.Product.MQ_PWD}@'
           f'{settings.Product.HOST}:{settings.Product.MQ_PORT}//',
    backend=f'redis://{settings.Product.HOST}:{settings.Product.REDIS_PORT}/2'
)


class Config:
    # 导入/注册 异步任务
    CELERY_IMPORTS = (
        'asynchronous.common_task'
    )
    CELERY_TIMEZONE = 'Asia/Shanghai'

    # 存储的结果被删除的时间（秒数，或者一个 timedelta 对象）
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    # 单个任务的运行时间限制，否则会被杀死（单位为：秒，windows 下无效）
    CELERYD_TASK_TIME_LIMIT = 60 * 60
    # 每个worker执行了多少任务就会死掉，默认是无限的
    CELERY_MAX_TASKS_PER_CHILD = 200

    # 执行任务并发工作进程/线程/绿色线程数量， 默认值为 cpu 内核数
    CELERY_CONCURRENCY = 2
    # celery worker每次去redis取任务的数量，默认值就是4
    CELERY_PREFETCH_MULTIPLIER = 4

    # 4.4.0 新增特性
    CONTROL_QUEUE_EXPIRES = None
    CONTROL_QUEUE_TTL = None

    # 声明交换机、队列以及交换机队列的绑定
    # CELERY_QUEUES = (
    #     Queue('default', Exchange('default'), routing_key='default'),
    #     Queue('infinite_worker', Exchange('infinite_worker'), routing_key='infinite_worker'),
    #     Queue('info', Exchange('project_logs', type='direct'), routing_key='info'),
    #     Queue('error', Exchange('project_logs', type='direct'), routing_key='error'),
    # )
    # CELERY_DEFAULT_QUEUE = 'default'
    # CELERY_DEFAULT_EXCHANGE = 'default'
    # CELERY_DEFAULT_ROUTING_KEY = 'default'

    # 配置文件中对异步任务进行与交换机、队列的绑定
    #   1. 默认交换机 "" 都是通过 direct 方式进行转发
    #   2. 所有的队列都默认绑定一个与队列名相同的 routing_key，以便默认交换机进行匹配转发
    #   3. 对于没有指定交换机名称的任务，都会发送给默认交换机 ""，由默认交换机 "" 进行转发到对应的队列中
    # CELERY_ROUTES = {
    #     将任务绑定到交换机上，需要指明 routing_key，根据 routing_key 进行路由
    #     'asynchronous.exchange_tasks.case2':
    #         {
    #             'exchange': 'infinite_worker',
    #             'routing_key': 'infinite_worker'
    #         },
    #     将任务直接绑定到队列中
    #       1. 未指明交换机，通过默认交换机 "" 进行转发给 info 队列
    #       2. 默认交换机会根据队列的名字进行 routing_key 匹配转发
    #       3. 默认每一个队列都绑定一个与名称相同的 routing_key
    #     'asynchronous.exchange_tasks.case3':
    #         {
    #             'queue': 'info',
    #         },
    # }

    # 配置定时任务
    # CELERYBEAT_SCHEDULE = {
    #     'beat_task_name': {
    #         'task': 'asynchronous.exchange_tasks.schedule',
    #         # 'schedule': crontab(minute='*/1', hour='*/6'),
    #         'schedule': timedelta(seconds=5),
    #         'args': "",
    #         # 指明交换机，根据 routing_key 转发
    #         'options': {
    #             'exchange': 'infinite_worker',
    #             'routing_key': 'infinite_worker'
    #         },
    #         # 指明 queue, 由默认交换机转发到此队列
    #         # 'options': {
    #         #     'queue': 'infinite_worker',
    #         # },
    #     }
    # }


c_app.config_from_object(Config)
