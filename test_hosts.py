from monitoring.net_utils import check_ping, check_http
import monitoring.config_loader as cl
import socket
from monitoring.timestamp import timestamp
import json
from pprint import pprint

config = cl.load_config()

hosts = config['hosts']

for domain in hosts.keys():
    print(domain)
    result = []
    check_arr = hosts[domain]

    try:
        ipaddr = socket.gethostbyname(domain)
    except Exception as e:
        print("Неможливо визначити IP-адресу {}! {}".format(domain, str(e)))
        exit()

    if ipaddr:
        print("IP-адреса: {}".format(ipaddr))

    for one_check in check_arr:
        if one_check == 'check_ping':
            print("Pinging {}: {}...\n".format(domain, ipaddr))
            result.append({'ping': check_ping(ipaddr)})
        elif one_check == 'check_http':
            print("Checking http://{}...\n".format(domain))
            result.append({'http': check_http(config, domain, 80)})
        elif one_check == 'check_https':
            print("Checking https://{}...\n".format(domain))
            result.append({'https': check_http(config, domain, 443)})
    domain_result = {'domain': domain, \
                     'timestamp': timestamp(), \
                     'results': result}
    print(domain_result)
    pprint(json.dumps(domain_result))
    with open(f'results/{domain}.json', 'w', encoding='utf-8') as f:
        json.dump(domain_result, f, ensure_ascii=False)
