from flask_script import Command

from models import init_db, drop_db


class InitDB(Command):
    init_db()


class ClearDB(Command):
    drop_db()
