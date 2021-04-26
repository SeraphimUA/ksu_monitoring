from monitoring.net_utils import check_ping, check_http
import monitoring.config_loader as cl
from monitoring.dns_tools import get_resolver, get_record, get_ip_addresses, check_dns
from monitoring.check_utils import check_result_status
from monitoring.timestamp import timestamp
import json
from pprint import pprint
from os import getcwd, path, makedirs

# load config from file config.yaml
config = cl.load_config()

# select list of hosts
hosts = config['hosts']

# domain loop
for domain in hosts.keys():
    print(domain)
    # insert here check_domain
    result = {}
    # select list of checks for host
    check_arr = hosts[domain]

    my_resolver = get_resolver(config)
    ips = get_ip_addresses(domain, my_resolver, False)
    print(ips)
    if not ips:
        print("Неможливо визначити IP-адресу {}!".format(domain))
        result['dns'] = {'status': 'fail', 'time_error': timestamp()}
        exit()

    ipaddr = ips[0]
    if ipaddr:
        print("IP-адреса: {}".format(ipaddr))

        for one_check in check_arr:
            if one_check == 'check_dns':
                print("Resolving {}...\n".format(domain))
                result['dns'] = check_dns(domain, my_resolver)
            if one_check == 'check_ping':
                print("Pinging {}: {}...\n".format(domain, ipaddr))
                result['ping'] = check_ping(ipaddr)
            elif one_check == 'check_http':
                print("Checking http://{}...\n".format(domain))
                result['http'] = check_http(config, domain, 80)
            elif one_check == 'check_https':
                print("Checking https://{}...\n".format(domain))
                result['https'] = check_http(config, domain, 443)

    domain_result = {'domain': domain, \
                     'timestamp': timestamp(), \
                     'results': result}
    print(domain_result)

    # check if result status changed. If yes, send alert
    check_result_status(domain, domain_result)

    # check if dir "results" exists. If not, make it
    pwd = getcwd()
    dir_result = path.join(pwd, 'results')
    if not path.exists(dir_result):
        make_dirs(dir_result)

    with open(f'{dir_result}/{domain}.json', 'w', encoding='utf-8') as f:
        json.dump(domain_result, f, ensure_ascii=False)
