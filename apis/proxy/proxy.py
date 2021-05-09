from flask import jsonify

from apis.proxy import api_proxy
from apps.proxy.models import SessionManager, Proxy
from common.utils import object_to_dict

session_manager = SessionManager()


@api_proxy.route('/getProxies', methods=['GET'])
def get_users():
    code = 200
    data = {}
    message = ''

    from apps.common.user.models import Admin, AdminLoginLog, SessionManager as cmSessionManager
    cmSession_manager = cmSessionManager()

    with cmSession_manager.session_execute() as session:
        admins = session.query(Admin).filter().all()
        data['admins'] = [object_to_dict(admin) for admin in admins]

    with session_manager.session_execute() as session:
        proxies = session.query(Proxy).filter().all()
        data['proxies'] = [object_to_dict(proxy) for proxy in proxies]

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)
