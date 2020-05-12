from datetime import datetime

from contextlib import contextmanager
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


@contextmanager
def session_maker(session=Session()):
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Users(Base):
    __tablename__ = 'users'

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
        return f'>>> openId: {self.openId}, nickName: {self.nickName}'


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # drop_db()
    init_db()
