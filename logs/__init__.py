import os
import time

import logging

ROOT_PATH = str(os.path.abspath(os.path.dirname(__file__)).split("flaskServer")[0]).replace("\\", "/")


class LogConfig:
    FORMAT = '%(asctime)s File "%(filename)s",line %(lineno)s %(levelname)s: %(message)s'
    FILEPATH = f'{ROOT_PATH}/flaskServer/logs'
    LEVEL = 'INFO'
    SUFFIX = '%Y-%m-%d_%H.log'
    WHEN = 'H'
    INTERVAL = '1'
    BACKUP_COUNT = '0'
    ENCODING = 'UTF-8'


class SafeFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", delay=0):

        current_time = time.strftime(LogConfig.SUFFIX, time.localtime())
        logging.FileHandler.__init__(self, filename + "." + current_time, mode, LogConfig.ENCODING, delay)

        self.mode = mode
        self.suffix = LogConfig.SUFFIX
        self.filename = os.fspath(filename)
        self.encoding = LogConfig.ENCODING
        self.suffix_time = current_time

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
        time_tuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix, time_tuple) or not os.path.exists(
                os.path.abspath(self.filename) + '.' + self.suffix_time):
            return 1
        else:
            return 0

    def build_base_filename(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        # if self.suffix_time != "":
        #     index = self.baseFilename.find("." + self.suffix_time)
        #     if index == -1:
        #         index = self.baseFilename.rfind(".")
        #     self.baseFilename = self.baseFilename[:index]

        current_time_tuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, current_time_tuple)
        self.baseFilename = os.path.abspath(self.filename) + "." + self.suffix_time

        if not self.delay:
            self.stream = open(self.baseFilename, self.mode, encoding=self.encoding)


def get_logger(app_name='default'):
    logger = logging.getLogger(app_name)

    formatter = logging.Formatter(LogConfig.FORMAT)

    handler = SafeFileHandler(LogConfig.FILEPATH + '/' + app_name + ".log")
    handler.setFormatter(formatter)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(stream)

    if LogConfig.LEVEL == 'info':
        logger.setLevel(logging.INFO)

    elif LogConfig.LEVEL == 'error':
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
