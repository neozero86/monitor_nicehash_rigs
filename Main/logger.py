import logging
import sys
from logging.handlers import TimedRotatingFileHandler

class Logger:

    configured = False

    def __init__(self, filename='logs/out.log'):
        if not Logger.configured:
            #logging.basicConfig(filename=filename,filemode='a',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            log_rotation_handler = TimedRotatingFileHandler(filename, when="d", interval=1, backupCount=10)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            log_rotation_handler.setFormatter(formatter)
            stream_handler = logging.StreamHandler(sys.stdout)
            logging.getLogger().addHandler(stream_handler)
            logging.getLogger().addHandler(log_rotation_handler)
            logging.getLogger().setLevel(logging.INFO)
            Logger.configured = True

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)

    def error(self, msg):
        logging.error(msg)