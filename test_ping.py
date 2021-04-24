from monitoring.net_utils import check_ping, check_http
import monitoring.config_loader as cl
import sys
import socket

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
print(timeout)
try:
    ipaddr = socket.gethostbyname(domain)
except Exception as e:
    print("<h2>Неможливо визначити IP-адресу {}!</h2><p>{}</p>".format(domain, str(e)))
    exit()

if ipaddr:
    print("<p>IP-адреса: {}</p>".format(ipaddr))

print("Ping {}...\n".format(ipaddr))
print(check_ping(ipaddr))

print("Check http://{}...\n".format(domain))
print(check_http(config, domain, port))
