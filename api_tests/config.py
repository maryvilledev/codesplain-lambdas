import json
from os.path import dirname, abspath

# Get the JSON config from the file system as a dictionary
def parse():
    config_path = dirname(abspath(__file__)) + '/config.json'
    config_file = open(config_path, 'r')
    config_dict = json.load(config_file)
    config_file.close()
    return config_dict

# Update the config file in the file system with the
# given key-value pair
def update(key, val):
    # Generate new config with the key-val pair
    config_path = dirname(abspath(__file__)) + '/config.json'
    config_file = open(config_path, 'r+w')
    config_dict = json.load(config_file)
    config_dict[key] = val
    new_config = json.dumps(config_dict)

    # Empty file contents and write new config
    config_file.seek(0)
    config_file.truncate()
    config_file.write(new_config)
    config_file.close()
