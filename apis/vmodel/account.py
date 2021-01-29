from flask import jsonify, request

from apis.vmodel import api_vmodel
from apps.proxy.models import SessionManager, Proxy
from common.utils import object_to_dict

session_manager = SessionManager()


@api_vmodel.route('/get_test', methods=['GET'])
def get_test():
    code = 200
    data = None
    msg = None

    res = {
        'code': code,
        'data': request.args,
        'msg': msg
    }

    return jsonify(res)


@api_vmodel.route('/post_test', methods=['POST'])
def post_test():
    code = 200
    data = None
    msg = None

    res = {
        'code': code,
        'data': request.form,
        'msg': msg
    }

    return jsonify(res)
