# import os
# import sys
# import logging
# from logging.handlers import RotatingFileHandler
#
# CWD = os.getcwd()
# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#
# log_path = os.path.join(CWD, 'logs/').replace('\\', '/')
# os.mkdir(log_path) if not os.path.exists(log_path) else ''
#
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(levelname)s: %(filename)s:%(lineno)d >>> %(message)s <<< %(asctime)s')
# log_file_handler = RotatingFileHandler(log_path, maxBytes=1024 * 1024 * 1, backupCount=3)
# log_file_handler.setFormatter(formatter)
# log_file_handler.setLevel(logging.INFO)
# logger.addHandler(log_file_handler)
#
# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)
# logger.addHandler(stream_handler)
#
# if __name__ == '__main__':
#     print(BASE_DIR)
