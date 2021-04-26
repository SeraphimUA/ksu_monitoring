from monitoring.net_utils import check_ping, check_http
import monitoring.dns_tools as dt
import monitoring.config_loader as cl
import sys
#import socket

if len(sys.argv) <= 1:
    print("Enter a domain name!")
    exit()
domain = sys.argv[1]
if len(sys.argv)>2:
    port = sys.argv[2]
    if port != '443' and port != '80':
        port = 80
    else:
        port = int(port)
else:
    port = 80
print(domain, port)

config = cl.load_config()
timeout = config['timeouts']['http']
#try:
#    ipaddr = socket.gethostbyname(domain)
#except Exception as e:
#    print("Неможливо визначити IP-адресу {}! {}".format(domain, str(e)))
#    exit()

my_res = dt.get_resolver(config)
ips = dt.get_record(domain, 'A', my_res)

if not ips:
    print(f"Неможливо визначити IP-адресу {domain}")
    exit()

for ipaddr in ips:
    print("<p>IP-адреса: {}</p>".format(ipaddr))

    print("Ping {}...\n".format(ipaddr))
    print(check_ping(ipaddr))

    print("Check http://{}...\n".format(domain))
    print(check_http(config, domain, port))
