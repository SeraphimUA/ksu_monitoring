import json
import re
import ipaddress
from .smtp_utils import send_alert
from .config_loader import write_log

# function checking if domain written correctly
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

# function checking if IP address written correctly
def check_ip(ipaddr):
    try:
        ipaddress.ip_address(ipaddr)
        return True
    except ValueError:
        return False

# function checking if status changed and sending an email if it did
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

        try:
            time_error_old = rc_old['results'][srv]['time_error']
        except KeyError:
            time_error_old = None

        error_new = result['results'][srv]['error'] if 'error' in result['results'][srv] else ''

        subject = ""
        msg = ""

        if status_new == 'fail' and status_old == 'ok':
            subject = f"{domain} {srv} ALERT!"
            msg = f"{domain} {srv} ALERT!\n{error_new}"
            write_log(f"{domain} {srv} failed. {error_new}")
            
        if status_new == 'ok' and status_old == 'fail':
            msg = subject = f"{domain} {srv} Recovery"
            write_log(f"{domain} {srv} recovered")

        # setting error time into its previous value
        if status_new == 'fail' and status_old == 'fail':
            result['results'][srv]['time_error'] = time_error_old

        if msg:
            send_alert(subject, msg)
