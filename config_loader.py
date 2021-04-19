from os import getcwd, path
from .timestamp import timestamp

import yaml
from pprint import pprint

default_config_filename = "config.yaml"
default_error_log = "error.log"

defaults = {
    "dns": {
        "resolvers": [
            "8.8.8.8"
        ],
        "check_www": True
    },
    "timeouts": {
        "job": 80,
        "dns": 2,
        "http": 2,
        "http_read": 5,
        "mail": 2,
        "cache": 900
    },
    "mail": {
        "ports": [25, 465, 587]
    },
    "web": {
        "max_redirects": 6,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "check_http": True,
        "check_https": True,
        "check_ipv4": True,
        "check_ipv6": True,
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
                if value[0].isdigit():
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

def load_config_from_file(filename=default_config_filename):
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

