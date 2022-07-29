import json
from singleton import Singleton
from collections import namedtuple

CONFIGURATION_FILENAME = 'Main/conf.json'

def file_to_named_tuple(filename):
    with open(filename) as data_file:
        c_ = json.load(data_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return c_


def load_constants():
    c_ = file_to_named_tuple(CONFIGURATION_FILENAME)
    return c_


c = load_constants()