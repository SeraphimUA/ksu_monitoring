import dns.resolver
from .config_loader import write_log
from .check_utils import check_ip
from .timestamp import timestamp

# set resolver from config
def get_resolver(config):
    dns_timeout = config['timeouts']['dns']
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = config['dns']['resolvers']
    return my_resolver

# get dns records info
def get_record(domain, rtype, my_resolver = None):
    a = []
    try:
        # if resolver not defined, use system resolver
        if my_resolver:
            answer = my_resolver.resolve(domain, rtype)
        else:
            answer = dns.resolver.resolve(domain, rtype)

        for i in answer.response.answer:
            for j in i.items:
                a.append(j.to_text())
#    except dns.resolver.NoAnswer:
    except Exception as err_msg:
        err_msg = str(err_msg)
        return None
    return a

# get all IP addresses for domain (IPv4 & IPv6 (if check_ipv6 set))
def get_ip_addresses(domain, my_resolver = None, check_ipv6=True):
    a = []
    i = get_record(domain, 'A', my_resolver)
    if i:
         for j in i:
             if check_ip(j):
                 a.append(j)    
    if check_ipv6:
        i = get_record(domain, 'AAAA', my_resolver)
        if i:
            for j in i:
                if check_ip(j):
                    a.append(j)
    return a

def check_dns(domain, my_resolver = None):
    a = get_record(domain, 'A', my_resolver)
    aaaa = get_record(domain, 'AAAA', my_resolver)
    ns = get_record(domain, 'NS', my_resolver)
    mx = get_record(domain, 'MX', my_resolver)
    if a:
        result = {'status': 'ok', 'A': a, 'AAAA': aaaa, 'NS': ns, 'MX': mx}
    else:
        result = {'status': 'fail', 'time_error': timestamp()}
    return result
