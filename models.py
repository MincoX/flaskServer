import threading
from datetime import datetime

from contextlib import contextmanager
from typing import Any

from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, Table, \
    ForeignKey, DateTime, func, Boolean, Text, LargeBinary

import settings
from manager import MODEL

engine = create_engine(
    f"mysql+mysqlconnector://{settings.config_map[MODEL].MYSQL_USER}:{settings.config_map[MODEL].MYSQL_PWD}"
    f"@{settings.config_map[MODEL].MYSQL_HOST}:{settings.config_map[MODEL].MYSQL_PORT}"
    f"/{settings.config_map[MODEL].DATABASE}",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=300,  # 连接池大小
    pool_timeout=20,  # 连接池中没有已建立的连接时，新建立 http 连接最多等待的时间
    pool_recycle=60 * 5,  # session 对象被重置，防止 mysql 清除建立的 http 连接后，session 对象还保持原有会话而报错
)

Base = declarative_base()
Session = sessionmaker(bind=engine)


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


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True)
    openId = Column(String(128), unique=True, nullable=False)
    username = Column(String(128), nullable=False, default='')
    password = Column(String(256), nullable=False, default='')
    nickName = Column(String(128), unique=False, nullable=True)
    gender = Column(Integer, default=0)
    avatarUrl = Column(String(256), nullable=True)
    auth_key = Column(String(256), nullable=True)
    active = Column(Boolean, default=True)

    language = Column(String(32), nullable=True)
    country = Column(String(128), nullable=True)
    province = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)
    birthday = Column(DateTime(timezone=True), nullable=True)

    phone = Column(String(128), nullable=True)
    email = Column(String(256), nullable=True)
    create_time = Column(DateTime(timezone=True), default=func.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f'>>> nickName: {self.nickName}, openId: {self.openId}'


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # drop_db()
    init_db()
