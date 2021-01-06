import os
import time

import logging

ROOT_PATH = str(os.path.abspath(os.path.dirname(__file__)).split("flaskServer")[0]).replace("\\", "/")


class LogConfig:
    LEVEL = 'INFO'
    ENCODING = 'UTF-8'
    FILEPATH = f'{ROOT_PATH}/flaskServer/logs'
    FORMAT = '%(asctime)s File "%(filename)s",line %(lineno)s %(levelname)s: %(message)s'


class SafeFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", delay=0):

        logging.FileHandler.__init__(self, filename, mode, LogConfig.ENCODING, delay)

        self.mode = mode
        self.filename = os.fspath(filename)
        self.encoding = LogConfig.ENCODING

    def emit(self, record):
        try:
            if self.check_base_filename():
                self.build_base_filename()

            logging.FileHandler.emit(self, record)

        except(KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_base_filename(self):

        if not os.path.exists(os.path.abspath(self.filename)):

            return True

        else:

            return False

    def build_base_filename(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        self.baseFilename = os.path.abspath(self.filename)

        if not self.delay:
            self.stream = open(self.baseFilename, self.mode, encoding=self.encoding)


def get_logger(app_name='default'):
    logger = logging.getLogger(app_name)
    logging.basicConfig(level=LogConfig.LEVEL, format=LogConfig.FORMAT)

    handler = SafeFileHandler(LogConfig.FILEPATH + '/' + app_name + ".log")
    handler.setFormatter(logging.Formatter(LogConfig.FORMAT))
    logger.addHandler(handler)

    if LogConfig.LEVEL == 'INFO':
        logger.setLevel(logging.INFO)

    elif LogConfig.LEVEL == 'ERROR':
        logger.setLevel(logging.ERROR)

    return logger


if __name__ == '__main__':
    logger = get_logger('wechat_mp')
    for i in range(0, 100):
        logger.debug('I\'m debug')
        logger.warning('I\'m warning')
        logger.info('I\'m info')
        logger.error('I\'m error')
        time.sleep(1)
