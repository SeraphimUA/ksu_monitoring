from os import getcwd, path
from .timestamp import timestamp

import yaml

default_config_filename = "config.yaml"
default_error_log = "error.log"

# define default config
defaults = {
    "dns": {
        "resolvers": [
            "8.8.8.8"   # external resolver to check work of domain outside local network
        ]
    },
    "ipv6": True,   # define if we work with IPv6 addresses
    "timeouts": {
        "dns": 2,
        "http": 5,
        "mail": 2
    },
    "mail": {
        "ports": [25, 465, 587]
    },
    "web": {
        "accept_language": "uk",
        "user_agent": "my_monitor/0.0.1",
    }
}

def write_log(strn, filename = default_error_log):
    with open(filename, 'a') as l:
        l.write(timestamp() + " " + strn + "\n")

def merge_dicts(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            if isinstance(value, str):
                if value.isdigit():
                    destination[key] = floor(value)
                elif value == "False":
                    destination[key] = False
                elif value == "True":
                    destination[key] = True
                else:
                    destination[key] = value
            else:
                destination[key] = value
    return destination

def load_config(filename=default_config_filename):
    pwd = getcwd()
    try:
        with open(filename) as f:
            config_from_file = yaml.safe_load(f)
            if not config_from_file:
                print(f"{timestamp()} Файл конфігурації не знайдено. " +
                      "Використовуються значення за замовчуванням\n")
                config = defaults
            else:
                config = merge_dicts(config_from_file, defaults)
    except FileNotFoundError:
        config = defaults
        write_log("Файл конфігурації не знайдено. Використовуються значення за замовчуванням")
    return config

