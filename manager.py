import datetime
from threading import Lock

from flask_script import Manager, Server

import settings
# from common import logger
from apps import create_app

MODEL = 'develop'
app = create_app(MODEL)

manager = Manager(app)
manager.add_command("runserver", Server(settings.config_map[MODEL].HOST, settings.config_map[MODEL].PORT))

if __name__ == '__main__':
    app.run(host=settings.config_map[MODEL].SERVER_HOST, port=settings.config_map[MODEL].PORT)
