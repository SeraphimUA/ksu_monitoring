import platform
import subprocess
import requests
from .timestamp import timestamp
from .config_loader import write_log

def check_ping(ip_addr):
    result = []
    try :
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '2', ip_addr]
        output = subprocess.check_output(command).decode().strip()
        result.append({"status": "ok"})

    except Exception as err_msg:
        result.append({"status": "fail", \
                       "time_error": timestamp(), \
                       "error": str(err_msg)})
        write_log(f"{ip_addr} ping failed. {str(err_msg)}")
    return result

def check_http(config, domain, port):
    result = []
    headers = {
               'User-Agent': config['web']['user_agent'],
               'Accept-Language': config['web']['accept_language'],
               'Accept-Encoding': 'gzip, deflate'
               }
    protocol = "https" if port == 443 else "http"
    url = f"{protocol}://{domain}:{port}/"
    p_timeout = config['timeouts']['http']
    try:
        r = requests.get(url, timeout = p_timeout, headers = headers)
        if r.status_code == 200:
            result.append({"status": "ok", "url": r.url, \
                           "status_code": r.status_code})
        else:
            result.append({"status": "fail", "url": r.url, \
                           "status_code": r.status_code})
            write_log(f"{r.url} failed. Status code: {r.status_code}")
    except Exception as err_msg:
        result.append({"status": "fail", \
                       "time_error": timestamp(), \
                       "error": str(err_msg)})
        write_log(f"{url} failed. {str(err_msg)}")
    return result
