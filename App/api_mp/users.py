import requests
from flask import request, jsonify

from App.api_mp import api_mp
from settings import MiniProgram
from common import wx_http, api_service
from models import session_maker

from models import Users


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
    user_info = request.json['userInfo']

    with session_maker() as session:
        user = session.query(Users).filter(Users.openId == user_info['openId']).first()
        if not user:
            user = Users(**user_info) if not user else ''
            session.add(user)

    res = {
        'code': 200,
        'data': None,
        'message': '用户信息保存成功！'
    }

    return jsonify(res)
