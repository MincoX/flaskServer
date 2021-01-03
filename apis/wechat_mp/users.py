from flask import request, jsonify

from apis.wechat_mp import api_mp
from apps.wechat_mp.config import MiniProgram
from apps.wechat_mp.models import SessionManager, UserInfo
from common import wx_http
from asynchronous import common_task
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
    message = 'success'

    user_info = request.json['userInfo']

    # 发送邮件
    common_task.mail_send.delay(
        subject='Mp',
        sender='MincoX',
        recipients=['903444601@qq.com'],
        body=f'Server-Mp, 新用户注册，用户信息： {user_info.__dict__}'
    )

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
    message = 'success'

    with session_manager.session_execute() as session:
        users = session.query(UserInfo).filter().all()
        data = [object_to_dict(user) for user in users]

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)


@api_mp.route('/sendMail', methods=['GET'])
def send_mail():
    code = 200
    data = None
    message = 'success'

    common_task.mail_send.delay(
        subject='Mp',
        sender='MincoX',
        recipients=['903444601@qq.com'],
        body='发送邮件测试'
    )

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)
