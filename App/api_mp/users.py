import requests
from flask import request, jsonify

from App.api_mp import api_mp
from settings import MiniProgram
from common import wx_http, api_service
from models import SessionManager, UserInfo
from common.utils import object_to_dict

session_manager = SessionManager()


@api_mp.route('/')
def hello_world():
    return 'hello world'


@api_mp.route('/getSession')
def get_session():
    js_code = request.args.get("code")
    url = f"https://api.weixin.qq.com/sns/jscode2session?" \
          f"appid={MiniProgram.AppId}&secret={MiniProgram.AppSec}&js_code={js_code}&grant_type=authorization_code"

    res = wx_http.handle_request(url)

    return jsonify(res)


@api_mp.route('/saveUserinfo', methods=['POST'])
def save_user():
    code = 200
    data = None
    message = ''

    user_info = request.json['userInfo']

    with session_manager.session_execute() as session:
        user = session.query(UserInfo).filter(UserInfo.openId == user_info['openId']).first()
        if not user:
            user = UserInfo(**user_info) if not user else ''
            session.add(user)
            message = '用户信息保存成功!'

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)


@api_mp.route('/getUsers', methods=['GET'])
def get_users():
    code = 200
    data = None
    message = ''

    with session_manager.session_execute() as session:
        users = session.query(UserInfo).filter().all()
        data = [object_to_dict(user) for user in users]

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)
