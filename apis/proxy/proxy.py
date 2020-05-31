from flask import request, jsonify

from apis.proxy import api_proxy
from apps.proxy.models import SessionManager, Proxy
from common.utils import object_to_dict

session_manager = SessionManager()


@api_proxy.route('/getProxies', methods=['GET'])
def get_users():
    code = 200
    data = None
    message = ''

    with session_manager.session_execute() as session:
        proxies = session.query(Proxy).filter().all()
        data = [object_to_dict(proxy) for proxy in proxies]

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)
