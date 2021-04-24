import dns.resolver
from .config_loader import write_log

def get_record(domain, rtype):
    a = []
    try:
        answer = dns.resolver.resolve(domain, rtype)
        for i in answer.response.answer:
            for j in i.items:
                a.append(j.to_text())
#    except dns.resolver.NoAnswer:
    except Exception as err_msg:
        print(domain + " " + rtype + " not resolved. ")
        print(err_msg)
    return a

def get_ip_addresses(domain, check_ipv6=True):
    a = get_record(domain, 'A')
    if check_ipv6:
        for i in get_record(domain, 'AAAA'):
            a.append(i)
    return a
