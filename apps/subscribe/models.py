import threading

from contextlib import contextmanager
from typing import Any

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Boolean, Date

import settings
from manager import MODEL

engine = create_engine(
    f"mysql+mysqlconnector://{settings.config_map[MODEL].MYSQL_USER}:{settings.config_map[MODEL].MYSQL_PWD}"
    f"@{settings.config_map[MODEL].HOST}:{settings.config_map[MODEL].MYSQL_PORT}"
    f"/subscribe",
    max_overflow=0,
    pool_size=300,
    pool_timeout=20,
    pool_recycle=60 * 5,
)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class SessionManager:
    """ 单例模式封装 session 的统一入口
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

    gender = Column(Integer, default=0)
    email = Column(String(256), nullable=True)
    phone = Column(String(128), nullable=True)
    id_card_num = Column(String(128), nullable=True)
    face_path = Column(String(128), nullable=False, default='')
    real_name = Column(String(128), nullable=False, default='')
    apply_date = Column(String(128), nullable=False, default='')

    # 0: 申请成功； 1：审核通过； 2：下发失败； 3：任务重试
    apply_status = Column(Integer, default=-1)
    retry_count = Column(Integer, default=0)
    fail_reason = Column(String(128), nullable=False, default='图片大小不符合要求')

    nick_name = Column(String(128), unique=False, nullable=True)
    avatar_url = Column(String(256), nullable=True)
    auth_key = Column(String(256), nullable=True)
    active = Column(Boolean, default=True)

    language = Column(String(32), nullable=True)
    country = Column(String(128), nullable=True)
    province = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)
    birthday = Column(DateTime(timezone=True), nullable=True)

    create_time = Column(DateTime(timezone=True), default=func.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f'>>> nick_name: {self.nick_name}, openId: {self.openId}'


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    openId = Column(String(128), unique=True, nullable=False)
    username = Column(String(128), unique=True, nullable=False, default='')
    password = Column(String(256), nullable=False, default='')

    create_time = Column(DateTime(timezone=True), default=func.now())


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # drop_db()
    init_db()

    session_manager = SessionManager()
    with session_manager.session_execute() as session:
        admin = session.query(Admin).filter(Admin.username == 'MincoX').first()
        if not admin:
            user = Admin(openId='1', username='MincoX', password='123456')
            session.add(user)

    print(' 数据库初始化成功 '.center(100, '*'))
