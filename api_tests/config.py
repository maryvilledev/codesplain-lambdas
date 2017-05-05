import json
from os.path import dirname, abspath

# Returns None if given dict contains all of the given keys,
# otherwise returns the first missing key.
def verify_keys(dict, keys):
    for key in keys:
        if key not in dict:
            return key
    return None

# Get the JSON config from the file system as a dictionary
def parse():
    config_path = dirname(abspath(__file__)) + '/config.json'
    with open(config_path, 'r') as config_file:
        try:
            config_dict = json.load(config_file)
        except IOError as error:
            raise IOError('your config.json file is missing:\n' + str(error))
        except ValueError as error:
            raise ValueError('your config.json has invalid JSON in it:\n' + str(error))

    # Make sure config file has all required keys
    missing_key = verify_keys(config_dict, [
        'url',
        'access_token',
        'snippet',
        'user_id',
        'invalid_snippet_key',
    ])
    if missing_key:
        raise ValueError('"%s" entry is missing from config.json' % missing_key)

    return config_dict

# Update the config file in the file system with the
# given key-value pair
def update(key, val):
    config_path = dirname(abspath(__file__)) + '/config.json'
    with open(config_path, 'r+w') as config_file:
        # Generate new config with the key-val pair
        config_dict = json.load(config_file)
        config_dict[key] = val
        new_config = json.dumps(config_dict, indent=2)

        # Empty file contents and write new config
        config_file.seek(0)
        config_file.truncate()
        config_file.write(new_config)
