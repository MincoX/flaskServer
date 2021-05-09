import json
import uuid
import datetime
import hashlib

from flask import jsonify, request
from flask_login import login_user, login_required, logout_user, current_user

from logs import get_logger
from asynchronous import common_task
from apis.common import api_common
from apps import login_manager
from apps.common.user.config import CommonUser
from apps.common.user.models import Session, SessionManager, Admin, AdminLoginLog

logger = get_logger('common_user')
session_manager = SessionManager()


@login_manager.user_loader
def load_user(admin_id):
    session = Session()
    try:
        return session.query(Admin).filter(Admin.id == admin_id).one()
    except Exception as e:
        logger.error('load_user error', e)
        return None
    finally:
        session.close()


@api_common.route('/')
@api_common.route('/user_login', methods=['POST'])
def login():
    request_data = json.loads(request.data)

    res = {
        'code': 200,
        'data': None,
        'msg': 'success'
    }

    with session_manager.session_execute() as session:

        account = session.query(Admin).filter(Admin.username == request_data.get('username')).first()
        if account:
            if account.password == hashlib.md5(
                    (request_data.get('password') + CommonUser.SECRET_KEY).encode()
            ).hexdigest():

                # 邮件提示
                common_task.mail_send.delay(
                    subject='vmodel',
                    sender='MincoX',
                    recipients=['903444601@qq.com'],
                    body=f'{request_data.get("username")} 用户登录！'
                )

                login_user(account)
                print("current_user >>> ", current_user)
                login_log = AdminLoginLog(
                    admin_id=account.id,
                    ip=request.environ.get('X-Real-IP', request.remote_addr),
                    server_url=request.url,
                    create_time=datetime.datetime.now(),
                )
                session.add(login_log)
                session.commit()
                session.close()

                res['data'] = {'token': str(uuid.uuid4())}

                return jsonify(res)

            else:
                res['code'], res['msg'] = 400, "用户名或密码错误"

                return jsonify(res)
        else:
            res['code'], res['msg'] = 400, "用户不存在，请先注册"

            return jsonify(res)


@api_common.route('/login_out', methods=['GET'])
@login_required
def login_out():
    logout_user()

    res = {
        'code': 200,
        'data': None,
        'msg': 'success'
    }

    return jsonify(res)


@api_common.route('/test', methods=['GET'])
@login_required
def test():
    print("current_user >>> ", current_user)

    res = {
        'code': 200,
        'data': None,
        'msg': 'success'
    }

    return jsonify(res)
