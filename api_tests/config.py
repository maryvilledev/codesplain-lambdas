import json
from os.path import dirname, abspath

def parse():
    config_path = dirname(abspath(__file__)) + '/config.json'
    config_dict = json.load(open(config_path, 'r'))
    return config_dict
