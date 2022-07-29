import logging
import sys

class Logger:

    configured = False

    def __init__(self, filename='logs/out.log'):
        if not Logger.configured:
            logging.basicConfig(filename=filename,filemode='a',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
            Logger.configured = True

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)

    def error(self, msg):
        logging.error(msg)