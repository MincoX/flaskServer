import threading
from datetime import datetime
from typing import Any

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, Table, \
    ForeignKey, DateTime, func, Boolean, Text, LargeBinary

import settings
from manager import MODEL

DATABASE = 'proxy_server'

engine = create_engine(
    f"mysql+mysqlconnector://{settings.config_map[MODEL].MYSQL_USER}:{settings.config_map[MODEL].MYSQL_PWD}"
    f"@{settings.config_map[MODEL].HOST}:{settings.config_map[MODEL].MYSQL_PORT}"
    f"/{DATABASE}",
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

protocol_map = {
    -1: '不可用',
    0: 'http',
    1: 'https',
    2: 'http/https'
}

nick_type_map = {
    -1: '不可用',
    0: '高匿',
    1: '匿名',
    2: '透明'
}


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


class Admin(Base):
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
    create_time = Column(DateTime(timezone=True), default=func.now())

    admin_id = Column(Integer, ForeignKey('admin.id'))
    # lazy=select, return all object,  lazy=dynamic, return query object
    admin = relationship('Admin', backref=backref('logs', lazy='select'))


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), default='')
    content = Column(Text)
    status = Column(Integer, default=0)
    create_time = Column(DateTime(timezone=True), default=func.now())

    admin_id = Column(Integer, ForeignKey('admin.id'))
    admin = relationship('Admin', backref=backref('messages', lazy='select'))


class Proxy(Base):
    __tablename__ = 'proxy'

    id = Column(Integer, primary_key=True)
    ip = Column(String(64))
    port = Column(String(64))
    # http:0, https:1, http/https:2
    protocol = Column(Integer, default=-1)
    # 高匿：0， 匿名：1， 透明：2
    nick_type = Column(Integer, default=-1)
    # speed : -1, ip 不可用
    speed = Column(Float, default=-1)
    area = Column(String(255), default='')
    score = Column(MutableDict.as_mutable(JSON), default={'score': 50, 'power': 0})
    # 代理 ip 的不可用域名列表
    disable_domain = Column(MutableList.as_mutable(JSON), default=[])
    origin = Column(String(128), default='')
    create_time = Column(DateTime(timezone=True), default=func.now())


class CeleryTask(Base):
    __tablename__ = 'celery_task'

    id = Column(Integer, primary_key=True)
    task_id = Column(String(128), default='')
    task_name = Column(String(128), default='')
    task_status = Column(Integer, nullable=True, default=1)
    start_time = Column(DateTime(timezone=True), nullable=True, default=func.now())
    end_time = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    times = Column(String(128), nullable=True, default='')
    harvest = Column(Integer, nullable=True, default=0)


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # drop_db()
    init_db()
