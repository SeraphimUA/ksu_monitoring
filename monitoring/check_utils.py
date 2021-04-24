import re
import ipaddress

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

def check_ip4(ipaddr):
    try:
        ipaddress.ip_network(ipaddr)
        return True
    except ValueError:
        return False
