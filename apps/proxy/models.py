import threading

from typing import Any
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, ForeignKey, DateTime, func, Text

import settings
from manager import MODEL
from apps.proxy import config

engine = create_engine(
    f"mysql+mysqlconnector://{settings.config_map[MODEL].MYSQL_USER}:{settings.config_map[MODEL].MYSQL_PWD}"
    f"@{settings.config_map[MODEL].HOST}:{settings.config_map[MODEL].MYSQL_PORT}"
    f"/{config.Proxy.DATABASE}",
    max_overflow=0,
    pool_size=300,
    pool_timeout=20,
    pool_recycle=60 * 5,
)

Base = declarative_base()
Session = sessionmaker(bind=engine)

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


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), default='')
    content = Column(Text)
    status = Column(Integer, default=0)
    create_time = Column(DateTime(timezone=True), default=func.now())


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
    score = Column(MutableDict.as_mutable(JSON), default={'score': config.Proxy.MAX_SCORE, 'power': 0})
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
