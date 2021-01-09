import json
from flask import request, jsonify

from logs import get_logger
from apis.wechat_mp import api_mp
from rabbitmq.RabbitMQ import new_routing
from apps.wechat_mp.config import MiniProgram
from apps.wechat_mp.models import SessionManager, UserInfo, Admin
from common import wx_http, face_detect
from asynchronous import common_task
from common.utils import object_to_dict, user_to_device

session_manager = SessionManager()
logger = get_logger('wechat_mp')


@api_mp.route('/')
def MincoX():
    return 'MincoX'


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
    data = {}
    message = 'success'

    register = False
    user_info = request.json['userInfo']

    with session_manager.session_execute() as session:
        user = session.query(UserInfo).filter(UserInfo.openId == user_info['openId']).first()
        if not user:
            user = UserInfo(
                nick_name=user_info.get('nickName'),
                gender=user_info.get('gender'),
                language=user_info.get('language'),
                city=user_info.get('city'),
                province=user_info.get('province'),
                country=user_info.get('country'),
                avatar_url=user_info.get('avatarUrl'),
                openId=user_info.get('openId')
            )
            session.add(user)
            message = '用户信息保存成功!'

            register = True

    if register:
        common_task.mail_send.delay(
            subject='Mp',
            sender='MincoX',
            recipients=['903444601@qq.com'],
            body=f'【MincoX】新用户注册，用户信息： {user_info} '
        )

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)


@api_mp.route('/uploadAvatar', methods=['POST'])
def upload_avatar():
    code = 200
    data = {}
    message = 'success'

    file = request.files.get('uploadAvatar')
    openid = request.form.get('openId')

    file_path = f"static/upload/wechat/{openid}.{file.filename.rpartition('.')[2]}"
    file.save(file_path)

    face_detector = face_detect.FaceDetect(file_path)
    face_path = face_detector.detect()
    if not face_path:
        message = face_detector.err_msg

    data['face_path'] = face_path
    with session_manager.session_execute() as session:
        user = session.query(UserInfo).filter(UserInfo.openId == openid).first()
        user.face_path = face_path

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)


@api_mp.route('/submitApply', methods=['POST'])
def submit_apply():
    code = 200
    data = {}
    message = 'success'

    data = json.loads(request.data)

    with session_manager.session_execute() as session:
        session.query(UserInfo).filter(UserInfo.openId == data.get('openId')).update(
            {
                "real_name": data.get("name"),
                "gender": data.get('gender'),
                "email": data.get('mail'),
                "phone": data.get('phoneNum'),
                "id_card_num": data.get('idNum'),
                "apply_date": data.get('applyDate'),
                "apply_status": 0,
            }
        )
        message = '申请成功，请等候邮件通知'

    logger.info(f' 用户 {data.get("name")} 提交申请')
    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)


@api_mp.route('/adminLogin', methods=['POST'])
def admin_login():
    code = 200
    data = {}
    message = 'success'

    data = json.loads(request.data)
    account = data.get('account')
    pwd = data.get('pwd')

    with session_manager.session_execute() as session:
        admin = session.query(Admin).filter(Admin.username == account).first()

        if not admin:
            code = 201
            message = '账号不存在，请检查后重试'
        else:
            if not pwd == admin.password:
                code = 202
                message = '账号或密码有误'

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)


@api_mp.route('/getUsers', methods=['GET'])
def get_users():
    code = 200
    data = {}
    message = 'success'

    request_data = request.args
    filter_type = request_data.get('filterType')

    with session_manager.session_execute() as session:
        users = session.query(UserInfo).filter(UserInfo.apply_status == filter_type).all()
        if len(users) >= 1:
            data = [object_to_dict(user) for user in users]

    res = {
        'code': code,
        'data': data,
        'msg': message
    }

    return jsonify(res)


@api_mp.route('/auditUser', methods=['POST'])
def audit_user():
    code = 200
    data = {}
    message = 'success'

    request_data = json.loads(request.data)
    openid = request_data.get('openId')
    operate = request_data.get('operate')

    with session_manager.session_execute() as session:
        user = session.query(UserInfo).filter(UserInfo.openId == openid).first()

        if operate == '2':
            user.apply_status = 2
            result = True
            message = '已拒绝下发用户'

            common_task.mail_send.delay(
                subject='Mp',
                sender='MincoX',
                recipients=[user.email],
                body=f'【MincoX】管理员拒绝了您 {user.apply_date} 的预约'
            )
            logger.info(f' 已拒绝用户 {user.real_name} 的下发 ')

        else:
            result, reason = user_to_device(user)
            if result:
                user.apply_status = 1
                message = '用户已成下发设备'
                common_task.mail_send.delay(
                    subject='Mp',
                    sender='MincoX',
                    recipients=[user.email],
                    body=f'【MincoX】恭喜你预约 {user.apply_date} 成功'
                )
                logger.info(f' 用户 {user.real_name} 下发成功，已发送邮件通知对方 ')

            else:
                message = reason
                user.fail_reason = reason

                # 利用 mq 实现任务延迟重试
                mq = new_routing('routingExchange', 'routingQueue', 'task')
                mq.routing_producer(json.dumps(object_to_dict(user)), 'task')

    res = {
        'code': code,
        'data': data,
        'msg': message,
        'status': result
    }

    return jsonify(res)
