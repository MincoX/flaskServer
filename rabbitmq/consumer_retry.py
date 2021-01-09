import json
import datetime

from logs import get_logger
from asynchronous import common_task
from common.utils import user_to_device
from common.mysql_pool import ConnMysql
from rabbitmq.RabbitMQ import new_routing, get_retry_count, fail_task_handle, retry_task_handle, DELAY_MAP

logger = get_logger('wechat_mp')


def call_back(channel, method, properties, body):
    # print(f'>>> 执行回调函数：channel {channel.__dict__}, \n'
    #       f'method {method.__dict__}, \n'
    #       f'properties {properties.__dict__}, \n'
    #       f'body {body}\n')

    message = body.decode().split('.')
    count = get_retry_count(properties)
    try:
        res = 1 / int(message[0])
        logger.info(f'业务处理成功 >>> {res}'.center(100, '*'))

    except ZeroDivisionError:
        if count < 3:
            retry_task_handle(mq, channel, method, properties, body)
            logger.info(f'任务执行失败, 消息已发送至延迟队列, {DELAY_MAP[get_retry_count(properties)] / 1000} '
                        f'秒后将进行第 {count + 1} 次重试 >>> {datetime.datetime.now()}'.center(100, '*'))

        else:
            fail_task_handle(mq, channel, method, properties, body)
            logger.warn(f'任务执行失败 >>> {datetime.datetime.now()}'.center(100, '*'))

    # 无论任务执行成功还是失败，都进行确认
    channel.basic_ack(delivery_tag=method.delivery_tag)
    # channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


def retry_face_to_device(channel, method, properties, body):
    # print(f'>>> 执行回调函数：channel {channel.__dict__}, \n'
    #       f'method {method.__dict__}, \n'
    #       f'properties {properties.__dict__}, \n'
    #       f'body {body}\n')

    user = json.loads(body.decode())
    count = get_retry_count(properties)
    result, message = user_to_device(user)

    if result:
        sql = "update user_info set apply_status = %s where openId = %s"
        conn = ConnMysql()
        res, err = conn.update(sql, params=(1, user.get('openId')))

        if err is not None:
            logger.warn(f' 用户 {user.get("real_name")} 已经下发设备，但 sql 执行失败用户下发状态未更新 '.center(100, '*'))

        else:
            logger.info(f' 用户 {user.get("real_name")} , 第 {count + 1} 次重试下发成功 '.center(100, '*'))

        common_task.mail_send.delay(
            subject='Mp',
            sender='MincoX',
            recipients=[user.get('email')],
            body=f'【MincoX】恭喜你预约 {user.get("apply_date")} 成功 （debug 第 {count + 1} 次重试） '
        )

    else:
        if count < 3:
            retry_task_handle(mq, channel, method, properties, body)
            logger.info(f' {user.get("real_name")}下发失败, 消息已发送至延迟队列, {DELAY_MAP[get_retry_count(properties)] / 1000}'
                        f' 秒后将进行第 {count + 1} 次重试 '.center(100, '*'))
        else:
            fail_task_handle(mq, channel, method, properties, body)
            logger.warn(f' 用户 {user.get("real_name")} 重试失败，任务进入失败队列 '.center(100, '*'))

    # 无论任务执行成功还是失败，都进行确认
    channel.basic_ack(delivery_tag=method.delivery_tag)


# 创建简单队列，简单队列默只用传入队列的名称
# mq = new_simple('simple')
# mq.simple_consumer(call_back=retry_face_to_device)

# 创建直连模式的消费者
mq = new_routing('routingExchange', 'routingQueue', 'task')
# mq = new_routing('routingExchange', 'routingQueue', ['info', 'warn'])
mq.routing_consumer(retry_face_to_device)
