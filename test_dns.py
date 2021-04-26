import monitoring.config_loader as cl
import monitoring.dns_tools as dt
import sys

if len(sys.argv) <= 1:
    print("Enter a domain name!")
    exit()
domain = sys.argv[1]
print(domain)

config = cl.load_config()
my_res = dt.get_resolver(config)
print(dt.get_record(domain, 'A', my_res))
print(dt.get_record(domain, 'NS', my_res))
print(dt.get_record(domain, 'AAAA', my_res))
print(dt.get_record(domain, 'MX', my_res))
