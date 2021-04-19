import json
import monitoring.config_loader as cl
import monitoring.dns_tools as dt
from monitoring.timestamp import timestamp
from pprint import pprint

config = cl.load_config_from_file()
# pprint(config)

results = []

# try:
with open('hosts.txt', 'r') as h:
    hosts = h.readlines()
    count = 0
    print('\n')
    for i in hosts:
        count += 1
        host = i.strip()
        print(f'{count} {host}')
        results.append({"domain": host})
        results.append({"timestamp": timestamp()})
        dns_rec = []
        dns_rec.append({"NS": dt.get_record(host, 'NS')})
        dns_rec.append({"IP4": dt.get_record(host, 'A')})
        dns_rec.append({"IP6": dt.get_record(host, 'AAAA')})
        dns_rec.append({"MAIL": dt.get_record(host, 'MX')})
        results.append({"DNS": dns_rec})
        ip_addr = dt.get_ip_addresses(host)
        if not ip_addr:
            write_log(domain + " " + rtype + " not resolved")
# TODO: send alert
        else:
            pprint(ip_addr)

# except:
#    print("Error happened")
results_json = json.dumps(results)
pprint(results_json)
