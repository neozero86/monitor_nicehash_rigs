import json
import os
from collections import namedtuple

class Configuration():
    def constants(filename = 'Main/conf.json'):
        if "CONF_FILE" in os.environ:
            filename='Main/conf_temp.json'
            with open(filename, 'w') as file:
                file.write(os.getenv('CONF_FILE'))
        with open(filename) as data_file:
            conf = json.load(data_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            rigs = {r.name: r for r in conf.rigs}
            devices = {k[2:].replace("_"," "): v for k ,v in conf.devices._asdict().items()}
            return conf, rigs, devices


  
