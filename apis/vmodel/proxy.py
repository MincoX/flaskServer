import json

from flask import jsonify, request

from apis.vmodel import api_vmodel
from apps.proxy.models import SessionManager, Proxy
from common.utils import object_to_dict

session_manager = SessionManager()


@api_vmodel.route('/getProxies', methods=['GET'])
def get_proxies():
    code = 200
    data = None
    msg = None

    with session_manager.session_execute() as session:
        proxies = session.query(Proxy).filter().all()
        data = [object_to_dict(proxy) for proxy in proxies]

    res = {
        'code': code,
        'data': data,
        'msg': msg
    }

    return jsonify(res)


@api_vmodel.route('/updateProxy', methods=['POST'])
def update_proxy():
    code = 200
    data = None
    msg = None

    req_data = json.loads(request.data)

    with session_manager.session_execute() as session:
        session.query(Proxy).filter(Proxy.id == req_data.get('id')).update(req_data)
        session.commit()

        msg = '修改成功'

    res = {
        'code': code,
        'data': data,
        'msg': msg
    }

    return jsonify(res)


@api_vmodel.route('/deleteProxy', methods=['POST'])
def delete_proxy():
    code = 200
    data = None
    msg = None

    req_data = json.loads(request.data)

    with session_manager.session_execute() as session:
        session.query(Proxy).filter(Proxy.id == req_data.get('id')).delete()
        session.commit()

        msg = '删除成功'

    res = {
        'code': code,
        'data': data,
        'msg': msg
    }

    return jsonify(res)
