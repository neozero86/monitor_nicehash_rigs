import json
import os
from collections import namedtuple
import importlib

class Configuration():
    PATH_TO_SOLUTION_MODULE = "Main.solution"
    def constants(filename = 'Main/conf.json'):
        if "CONF_FILE" in os.environ:
            filename='Main/conf_temp.json'
            with open(filename, 'w') as file:
                file.write(os.getenv('CONF_FILE'))
        with open(filename) as data_file:
            conf = json.load(data_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            rigs_pre = {r.name: r for r in conf.rigs}
            rigs = {}
            for name, rig in rigs_pre.items():
                rig_dict = rig._asdict()
                if ("id" not in rig_dict):
                    rig_dict["id"] = name
                rigs[name] = rig_dict
            devices = {k[2:].replace("_"," "): v for k ,v in conf.devices._asdict().items()}
            if hasattr(conf, 'delay_time'):
                delay_time = {k: v for k, v in conf.delay_time._asdict().items()}
            else:
                delay_time = {}
            solution_map = {k: v for k, v in conf.error_management._asdict().items()}
            for k, v in solution_map.items():
                for i in range(len(v)):
                    module = importlib.import_module(Configuration.PATH_TO_SOLUTION_MODULE + "." + camel_to_snake(v[i]))
                    if (v[i] in delay_time):
                        v[i] = getattr(module, v[i])(delay_time[v[i]])
                    else:
                        v[i] = getattr(module, v[i])()
            return conf, rigs, devices, solution_map

def camel_to_snake(s):
    return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')
  
