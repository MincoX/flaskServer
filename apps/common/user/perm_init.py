import hashlib


from logs import get_logger
from apps.common.user.config import CommonUser
from models import Session, Admin, Perm, Role

logger = get_logger('common_user')

rel_role_perm = {
    'role1': 'base',
    'role2': ['base', 'do_setting'],
    'role3': ['base', 'do_setting', 'do_auth'],
}


def init_system():
    session = Session()

    if session.query(Perm).first():
        return True

    perms = [
        Perm(name='基础用户', slug='base'),
        Perm(name='配置系统', slug='do_setting'),
        Perm(name='权限分配', slug='do_auth'),
    ]

    roles = [
        Role(name='普通管理员', slug='role1'),
        Role(name='系统管理员', slug='role2'),
        Role(name='超级管理员', slug='role3'),
    ]

    session.add_all(perms)
    session.add_all(roles)
    session.commit()

    for role in roles:
        for perm in perms:
            if perm.slug in rel_role_perm[role.slug]:
                role.perms.append(perm)

    admin = Admin(
        username=CommonUser.ADMIN_NAME,
        password=hashlib.md5((CommonUser.ADMIN_PASSWORD + CommonUser.SECRET_KEY).encode()).hexdigest(),
    )

    session.add(admin)
    session.commit()

    role3 = session.query(Role).filter(Role.slug == 'role3').one()
    admin.roles.append(role3)

    session.commit()
    session.close()

    logger.info('init system')


if __name__ == '__main__':
    init_system()
