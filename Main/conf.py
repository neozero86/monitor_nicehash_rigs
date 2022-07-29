import json
from collections import namedtuple

class Configuration():
    def constants(filename = 'Main/conf.json'):
        with open(filename) as data_file:
            conf = json.load(data_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            rigs = {k[2:]: v for k ,v in conf.rigs._asdict().items()}
            devices = {k[2:].replace("_"," "): v for k ,v in conf.devices._asdict().items()}
            return conf, rigs, devices


  
