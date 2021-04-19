import dns.resolver
from .config_loader import write_log

def get_record(domain, rtype):
    a = []
    try:
        answer = dns.resolver.resolve(domain, rtype)
        for i in answer.response.answer:
            for j in i.items:
                a.append(j.to_text())
    except dns.resolver.NoAnswer:
        print(domain + " " + rtype + " not resolved")
    return a

def get_ip_addresses(domain):
    a = []
    a.append(get_record(domain, 'A'))
    a.append(get_record(domain, 'AAAA'))
    return a
