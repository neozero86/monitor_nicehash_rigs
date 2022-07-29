import json
import logging
import os
from singleton import Singleton
from collections import namedtuple 


@Singleton
class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)

    def error(self, msg):
        logging.error(msg)


logger = Logger.instance()

CONFIGURATION_FILENAME = 'conf.json'


def file_to_named_tuple(filename):
    with open(filename) as data_file:
        c_ = json.load(data_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return c_


def load_constants():
    c_ = None
    try:
        c_ = file_to_named_tuple(CONFIGURATION_FILENAME)
    except FileNotFoundError as e:
        logger.error(e)
    return c_


c = load_constants()