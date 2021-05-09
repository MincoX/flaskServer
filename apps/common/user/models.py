import threading

from typing import Any
from flask_login import UserMixin
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Boolean, Table, ForeignKey, LargeBinary

import settings
from manager import MODEL
from apps.common.user.config import CommonUser

engine = create_engine(
    f"mysql+mysqlconnector://{settings.config_map[MODEL].MYSQL_USER}:{settings.config_map[MODEL].MYSQL_PWD}"
    f"@{settings.config_map[MODEL].HOST}:{settings.config_map[MODEL].MYSQL_PORT}"
    f"/{CommonUser.DATABASE}",
    max_overflow=0,
    pool_size=300,
    pool_timeout=20,
    pool_recycle=60 * 5,
)

Base = declarative_base()
Session = sessionmaker(bind=engine)

rel_admin_role = Table(
    'rel_admin_role', Base.metadata,
    Column('admin_id', Integer, ForeignKey('admin.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

rel_role_perm = Table(
    'rel_role_perm', Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('perm_id', Integer, ForeignKey('perm.id'))
)


class SessionManager:
    """
    单例模式封装 session 的统一入口
    """
    _lock = threading.Lock()

    def __new__(cls) -> Any:
        if not hasattr(cls, '_instance'):
            with SessionManager._lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        self.session = Session()

    @contextmanager
    def session_execute(self):
        try:
            yield self.session
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    slug = Column(String(32), unique=True, nullable=False)

    admins = relationship('Admin', secondary=rel_admin_role, back_populates='roles')
    perms = relationship('Perm', secondary=rel_role_perm, back_populates='roles')


class Perm(Base):
    __tablename__ = 'perm'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    slug = Column(String(32), unique=True, nullable=False)

    roles = relationship('Role', secondary=rel_role_perm, back_populates='perms')


class Admin(UserMixin, Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    active = Column(Boolean, default=True)
    header = Column(LargeBinary, nullable=True)
    auth_key = Column(String(256), default='')
    birthday = Column(DateTime(timezone=True), nullable=True)
    address = Column(String(128), nullable=True, default='')
    phone = Column(String(128), nullable=True, default='')
    email = Column(String(256), nullable=True, default='')
    create_time = Column(DateTime(timezone=True), default=func.now())

    roles = relationship('Role', secondary=rel_admin_role, back_populates='admins')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_perms(self):
        perms = []
        for role in self.roles:
            for perm in role.perms:
                perms.append((perm.slug, perm.name))
        return list(set(perms))

    def __repr__(self):
        return f'{self.id}:{self.username}'


class AdminLoginLog(Base):
    __tablename__ = 'admin_login_log'

    id = Column(Integer, primary_key=True)
    ip = Column(String(32), default='127.0.0.1')
    server_url = Column(String(256), default='')
    create_time = Column(DateTime(timezone=True), default=func.now())

    admin_id = Column(Integer, ForeignKey('admin.id'))
    # lazy=select, return all object,  lazy=dynamic, return query object
    admin = relationship('Admin', backref=backref('logs', lazy='select'))


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # drop_db()
    init_db()

    from perm_init import init_system

    init_system()

    print(' 数据库初始化成功 '.center(100, '*'))
