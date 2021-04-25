import json
import re
import ipaddress
from .smtp_utils import send_alert

def check_domain(domain):
    if len(domain) < 3:
        return False
    if len(domain) > 255:
        return False
    if domain.count('.') == 0:
        return False
    includedomain = domain.split('.')
    for k in includedomain:
        if k == '':
            return False
        if len(k) > 63:
            return False
        if re.search('[^a-z0-9\-]', k):
            return False
        if (k[0] == '-') or (k[len(k)-1] == '-'):
            return False
    return True

def check_ip(ipaddr):
    try:
        ipaddress.ip_address(ipaddr)
        return True
    except ValueError:
        return False

def check_result_status(domain, result):
    try:
        with open(f"results/{domain}.json",'r',encoding='utf-8') as r:
            rc_old = json.load(r)
    except FileNotFoundError:
        rc_old = {}

    for srv in result['results']:
        status_new = result['results'][srv]['status']
        try:
            status_old = rc_old['results'][srv]['status']
        except KeyError:
            status_old = 'ok'

        msg = ""
        if status_new == 'fail' and status_old == 'ok':
            msg = f"{domain} {srv} ALERT!"
            
        if status_new == 'ok' and status_new == 'fail':
            msg = f"{domain} {srv} Recovery"

        if msg:
            print(msg)
            send_alert(msg, msg)
