#!/usr/bin/env python3
import cgi
import html
import sys
import codecs
import platform
import subprocess
import socket
import ipaddress
import re

def check_domain(domain):
    if len(domain) < 3:
        return False
    if len(domain) > 255:
        return False
    if domain.count('.') == 0:
        return False
    includedomain = domain.split('.')
    for k in includedomain:
        if k == '':
            return False
        if len(k) > 63:
            return False
        if re.search('[^a-z0-9\-]', k):
            return False
        if (k[0] == '-') or (k[len(k)-1] == '-'):
            return False
    return True

def check_ipv4(ipaddr):
    try:
        ipaddress.IPv4Address(ipaddr)
    except ValueError:
        return False
    return True

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()
host1 = form.getfirst("p_host", "")
host1 = html.escape(host1)

# check host - length, space, special symbols

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Моніторинг</title>
        </head>
        <body>""")

print("<h1>Оброблення даних форми!</h1>")


if host1 :
    print("<p>Платформа: {}</p>".format(platform.system().lower()))
    if check_ipv4(host1):
        domain = ""
        ipaddr = host1
        print("<p>IP-адреса: {}</p>".format(ipaddr))
    elif check_domain(host1):
        domain = host1
        ipaddr = ""
        print("<p>Доменне ім'я: {}</p>".format(domain))
        try :
            ipaddr = socket.gethostbyname(domain)
            if ipaddr :
                print("<p>IP-адреса: {}</p>".format(ipaddr))
        except Exception as e:
            print("<h2>Неможливо визначити IP-адресу {}!</h2><p>{}</p>".format(domain, str(e)))
    else: 
        print("<h2>{} Некоректне доменне ім'я!</h2>".format(host1))
        domain = ipaddr = ""

    if ipaddr:
        try :
            param = '-n' if platform.system().lower()=='windows' else '-c'
            command = ['ping', param, '2', ipaddr]
            output = subprocess.check_output(command).decode().strip()
            print("<pre>{}</pre>".format(output))
#          if rc == 0 :
#              print("<h2>Success!</h2>")
#          else :
#              print("<h2>Fail!</h2>")
        except Exception as e2:
            print("<h2>Ping {} fail!</h2><p>{}</p>".format(ipaddr, str(e2)))

else :
   print("<p>Доменне ім'я не задано</p>")


print("""</body>
        </html>""")
