import json
import gevent.monkey

gevent.monkey.patch_all()

import requests


def handle_request(url, data=None, method="GET"):
    """
    微信统一请求接口
    :param url:
    :param data:
    :param method:
    :return:
    """
    if method == "GET":
        res = requests.get(url, params=data)
        if res.status_code == 200:
            # {"session_key":"4cR1DbB5qtoHgbvcREDDLQ==","openid":"oNdi55UhLTtt4KCKIVqzBT4eQyg4"}
            return handle_success(res.content.decode())
        else:
            # {"errcode":40029,"errmsg":"invalid code, hints: [ req_id: nKDBFKXIRa-n_ ]"}
            return handle_error(res)

    if method == "POST":
        res = requests.post(url, data=data)
        if res.status_code == 200:
            # {"session_key":"4cR1DbB5qtoHgbvcREDDLQ==","openid":"oNdi55UhLTtt4KCKIVqzBT4eQyg4"}
            return handle_success(res.content.decode())
        else:
            # {"errcode":40029,"errmsg":"invalid code, hints: [ req_id: nKDBFKXIRa-n_ ]"}
            return handle_error(res)


def handle_response(res):
    if res.status_code == 200:
        return handle_success(res)
    else:
        return handle_error(res)


def handle_success(res):
    res = {
        "code": 200,
        "data": json.loads(res),
        "msg": "请求成功！"
    }

    return res


def handle_error(res):
    res = {
        "code": res.errcode,
        "data": json.loads(res),
        "msg": res.errmsg
    }

    return res
