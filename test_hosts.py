from monitoring.net_utils import check_ping, check_http
import monitoring.config_loader as cl
from monitoring.dns_tools import get_resolver, get_record, get_ip_addresses, check_dns
from monitoring.check_utils import check_result_status
from monitoring.timestamp import timestamp
import json
from pprint import pprint
from os import getcwd, path, makedirs
from datetime import datetime, timedelta
import sys

my_config = "config.yaml"
if len(sys.argv)>1:
    my_config = sys.argv[1]

if not path.exists(my_config):
    print(f"Файл конфігугації {my_config} не знайдено.")
    exit()

# load config from file config.yaml
config = cl.load_config(my_config)

# debug print
debug = config['debug'] or False;

# select list of hosts
hosts = config['hosts']

# domain loop
for domain in hosts.keys():
    print(domain) if debug else None
    # insert here check_domain
    result = {}
    # select list of checks for host
    check_arr = hosts[domain]

    my_resolver = get_resolver(config)
    ips = get_ip_addresses(domain, my_resolver, False)
    print(ips) if debug else None
    if not ips:
        print(f"Неможливо визначити IP-адресу {domain}!") if debug else None
        result['dns'] = {'status': 'fail', 'time_error': timestamp()}
    else:
        ipaddr = ips[0]

    if ipaddr:
        print(f"IP-адреса: {ipaddr}") if debug else None

        for one_check in check_arr:
            if one_check == 'check_dns':
                print(f"Resolving {domain}...\n") if debug else None
                result['dns'] = check_dns(domain, my_resolver)
            if one_check == 'check_ping':
                print(f"Pinging {domain}: {ipaddr}...\n") if debug else None
                result['ping'] = check_ping(ipaddr)
            elif one_check == 'check_http':
                print(f"Checking http://{domain}...\n") if debug else None
                result['http'] = check_http(config, domain, 80)
            elif one_check == 'check_https':
                print(f"Checking https://{domain}...\n") if debug else None
                result['https'] = check_http(config, domain, 443)
            elif one_check == 'chart_data_http':
                print(f"Save data for chart http...\n") if debug else None
                now = datetime.now()
                yesterday = now - timedelta(days=2)
                time_check = f"Date({now.year},{(now.month - 1):02},{now.day:02},{now.hour:02},{now.minute:02})"
                time_yesterday = f"Date({yesterday.year},{(yesterday.month - 1):02},{yesterday.day:02},{yesterday.hour:02},{yesterday.minute:02})"
                check_status = 1 if result['http']['status'] == 'ok' else 0
                latency_check = result['http']['latency'] if 'latency' in result['http'] else 0

                # check if dir "charts_data" exists. If not, make it
                pwd = getcwd()
                dir_result = path.join(pwd, 'charts_data')
                if not path.exists(dir_result):
                    makedirs(dir_result)

                fname = f"{domain}.http.data"
                try:
                    with open(f'{dir_result}/{fname}', 'r') as f1:
                        data1 = f1.readlines()
                except:
                    data1 = []

                with open(f'{dir_result}/{fname}', 'w') as f2:
                    for line in data1:
                        d = line.split()[0]
                        if d >= time_yesterday:
                            f2.write(line)
                    f2.write(f"{time_check} {check_status} {latency_check}\n")

    domain_result = {'domain': domain, \
                     'timestamp': timestamp(), \
                     'results': result}

    # check if result status changed. If yes, send alert
    check_result_status(domain, domain_result)

    # check if dir "results" exists. If not, make it
    pwd = getcwd()
    dir_result = path.join(pwd, 'results')
    if not path.exists(dir_result):
        makedirs(dir_result)

    with open(f'{dir_result}/{domain}.json', 'w', encoding='utf-8') as f:
        json.dump(domain_result, f, ensure_ascii=False)
