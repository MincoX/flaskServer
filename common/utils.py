import re
import json
import time
import random
from datetime import datetime, timedelta

# from common import logger
from sqlalchemy.orm import class_mapper


def object_to_dict(obj):
    """
    以字典的形式返回数据模型对象的属性
    :param obj:
    :return:
    """

    def parse(o, c):
        r = getattr(o, c)

        if isinstance(r, datetime):
            return r.strftime('%Y-%m-%d %H:%M:%S')

        return r

    columns = [c.key for c in class_mapper(obj.__class__).columns]
    data = {c: parse(obj, c) for c in columns}

    return data


def object_to_list(obj):
    """
    以列表的形式返回数据模型对象的属性
    :param obj:
    :return:
    """

    def parse(o, c):
        r = getattr(o, c)

        if isinstance(r, datetime):
            return r.strftime('%Y-%m-%d %H:%M:%S')

        return r

    columns = [c.key for c in class_mapper(obj.__class__).columns]
    data = [parse(obj, c) for c in columns]

    return data


def hour_range(start_date=datetime.today().strftime("%Y-%m-%d") + ' 00',
               end_date=(datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + ' 00'
               ):
    """
    获取时间段中的每个整点时间刻，返回列表
    :param start_date:
    :param end_date:
    :return:
    """
    hours = []
    hour = datetime.strptime(start_date, "%Y-%m-%d %H")
    date = start_date[:]
    while date <= end_date:
        hours.append(date)
        hour = hour + timedelta(hours=1)
        date = hour.strftime("%Y-%m-%d %H")

    return hours


def calculate_time_countdown(end):
    """
    计算两个时间差，返回时间倒计时
    :param end:
    :return:
    """
    start = datetime.now()
    end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    start = time.mktime(start.timetuple()) * 1000 + start.microsecond / 1000
    end = time.mktime(end.timetuple()) * 1000 + end.microsecond / 1000

    total_seconds = (end - start) / 1000
    hours = int(total_seconds / 3600)
    days = int(hours / 24)
    minutes = int((total_seconds / 60) % 60)
    seconds = int(total_seconds % 60)

    return total_seconds, days, hours, minutes, seconds


def user_to_device(user_obj):
    """ 模拟将用户下发至设备
    :param user_obj:
    :return:
    """
    message = None

    reason_map = {
        0: "网络不稳定， 用户下发失败",
        1: "人员信息有误， 用户下发失败",
        2: "图片尺寸不符合要求， 用户下发失败"
    }

    if random.randint(0, 99) % 2 == 0:
        result = True
    else:
        result = False
    message = reason_map.get(random.randint(0, 2))

    return result, message
