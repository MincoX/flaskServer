import json
import types
import logging
import traceback
import importlib

from flask import request, abort
from flask_login import current_user

from models import Session


class Service:

    def __init__(self, session):
        self.session = session


class ApiService:

    def __init__(self, func):
        self.session = Session()
        self.func = func

    def func_decorate(self, *args, **kwargs):
        try:
            service = Service(self.session)
            return self.func(service, *args, **kwargs)

        except Exception as e:
            print(e)
            logging.error(traceback.format_exc(limit=None))

        finally:
            self.session.close()

    def __call__(self, *args, **kwargs):
        return self.func_decorate(*args, **kwargs)


# def check_perms(session, perms):
#     if not perms:
#         perms = ['base']
#
#     if current_user.__tablename__ != 'admin':
#         abort(403)
#
#     current_admin = session.query(Admin).filter(Admin.id == current_user.id).one()
#     perm_slugs = set([slug for slug, name in current_admin.get_perms()])
#
#     return perm_slugs >= set(perms)
#
#
# def permission_api_service(perms=None):
#     session = Session()
#
#     def func_wrapper(func):
#
#         def _wrapper(*args, **kwargs):
#             if current_user.__tablename__ == 'admin':
#                 if not check_perms(session, perms):
#                     return json.dumps({
#                         'status': 0,
#                         'message': '您没有权限，可以联系超级管理员升级角色！'
#                     })
#             try:
#                 serve = Service(session)
#                 return func(serve, *args, **kwargs)
#             except Exception as e:
#                 logger.error(e)
#                 logging.error(traceback.format_exc())
#                 return json.dumps({
#                     'status': 0,
#                     'message': '网络拥塞，请求失败！'
#                 })
#             finally:
#                 session.close()
#
#         return _wrapper
#
#     return func_wrapper
#
#
# def service_view(slug):
#     module_name, func_name = slug.split('.')
#
#     if request.method == 'GET':
#         module = importlib.import_module(f'App.api_v1.{module_name}')
#         service_obj = getattr(module, f'get_{func_name}')
#         ret = service_obj(**request.args.to_dict())
#     else:
#         module = importlib.import_module(f'App.api_v1.{module_name}')
#         service_obj = getattr(module, f'post_{func_name}')
#
#         ret = service_obj(**request.args.to_dict())
#
#     return ret


if __name__ == '__main__':
    # module = importlib.import_module('App.api_v1.dashboard')
    # func = module.get_navigate
    # print(func)
    # print(module)
    pass
