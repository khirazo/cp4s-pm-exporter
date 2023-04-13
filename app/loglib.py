'''
Created on 2023/04/13

@author: khrz
'''
from logging import Formatter, getLogger, INFO, DEBUG
from logging.handlers import RotatingFileHandler

LOG_PATH = '../store/log/app.log'
# 100 K bytes
MAX_BYTES = 100 * 1024
# retention file count
RET_FILES = 9

handler = None
applog = None

if not handler:
    handler = RotatingFileHandler(
        LOG_PATH,
        maxBytes=MAX_BYTES,
        backupCount=RET_FILES,
        encoding='utf-8')
    formatter = Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

if not applog:
    applog = getLogger()
    applog.addHandler(handler)
    applog.setLevel(INFO)
    # applog.setLevel(DEBUG)
