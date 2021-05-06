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
import requests
import dns.resolver
from datetime import datetime

def timestamp():
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"

# check if domain written correctly
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

# check if there is IP address written in the form
def check_ip(ipaddr):
    try:
        ipaddress.ip_address(ipaddr)
    except ValueError:
        return False
    return True

def check_http(domain, port):
    result = {}
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
               'Accept-Language': 'uk',
               'Accept-Encoding': 'gzip, deflate'
               }
    protocol = "https" if port == 443 else "http"
    url = f"{protocol}://{domain}:{port}/"
    p_timeout = 10
    try:
        r = requests.get(url, timeout = p_timeout, headers = headers)
        if r.status_code == 200:
            result = {"status": "ok", "url": r.url, \
                      "status_code": r.status_code}
        else:
            result = {"status": "fail", "url": r.url, \
                      "time_error": timestamp(), \
                      "status_code": r.status_code}
    except Exception as err_msg:
        result = {"status": "fail", \
                  "time_error": timestamp(), \
                  "error": str(err_msg)}
    return result

def get_record(domain, rtype):
    a = []
    try:
        answer = dns.resolver.resolve(domain, rtype)
        for i in answer.response.answer:
            for j in i.items:
                a.append(j.to_text())
    except:
        pass 
    return a

def check_dns(domain):
    a = get_record(domain, 'A')
    aaaa = get_record(domain, 'AAAA')
    ns = get_record(domain, 'NS')
    mx = get_record(domain, 'MX')
    if a:
        result = {'status': 'ok', 'A': a, 'AAAA': aaaa, 'NS': ns, 'MX': mx}
    else:
        result = {'status': 'fail', 'time_error': timestamp()}
    return result

if __name__ == '__main__':
    # prepare html
    # set utf-8
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    # read data from the form
    form = cgi.FieldStorage()
    host1 = form.getfirst("p_host", "")[:100]
    host1 = html.escape(host1, quote=True)

    p_check_ping = html.escape(form.getfirst("p_check_ping", "1"), quote=True)
    p_check_dns = html.escape(form.getfirst("p_check_dns", ""), quote=True)
    p_check_http = html.escape(form.getfirst("p_check_http", ""), quote=True)
    p_check_https = html.escape(form.getfirst("p_check_https", ""), quote=True)

    # check host - length, space, special symbols

    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Моніторинг сервісів</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>


<nav class="navbar navbar-expand-lg nav-pills" style="background-color: #ccd9d9;">
  <a class="nav-link active" aria-current="page" href="/">Моніторинг сервісів</a>
  <a class="nav-link" href="/cgi-bin/result.py">Сервіси ХДУ - загальний статус</a>
  <a class="nav-link" href="/cgi-bin/charts.py">Графіки</a>
</nav>

<div style="margin:20px">

""")

    print(f"<h1>Результат перевірки {host1}</h1>")


    if host1 :
        print("<p>Платформа: {}</p>".format(platform.system().lower()))
        if check_ip(host1):
            domain = ""
            ipaddr = host1
            print("<p>IP-адреса: {}</p>".format(ipaddr))
        elif check_domain(host1):
            domain = host1
            ipaddr = ""
            print("<p>Доменне ім'я: {}</p>".format(domain))
            # resolve IP address for domain
            try :
                ipaddr = socket.gethostbyname(domain)
                if ipaddr :
                    print("<p>IP-адреса: {}</p>".format(ipaddr))
            except Exception as e:
                print("<h2>Неможливо визначити IP-адресу {}!</h2><p>{}</p>".format(domain, str(e)))
        else: 
            print("<h2>{} Некоректне доменне ім'я!</h2>".format(host1))
            domain = ipaddr = ""

        if ipaddr and p_check_ping:
            # check ping
            try :
                param = '-n' if platform.system().lower()=='windows' else '-c'
                command = ['ping', param, '2', ipaddr]
                output = subprocess.check_output(command).decode().strip()
                print("<h2>Ping Success!</h2>")
                print("<pre>{}</pre>".format(output))
            except Exception as e2:
                print("<h2>Ping {} Fail!</h2><p>{}</p>".format(ipaddr, str(e2)))

        if domain:
            if p_check_dns:
                # check dns
                rc = check_dns(domain)
                if rc['status'] == 'ok':
                    print(f"<h2>DNS Success!</h2>")
                    print('<table style="width: 400px;padding: 10px;margin: 10px;">')
                    for r in ['A','AAAA','NS','MX']:
                        if rc[r]:
                            print(f'<tr><td style="background-color: #4caf50;color: white;vertical-align:top; padding:5px;">{r}:</td><td>')
                            for a in rc[r]:
                                print(f"{a}<br/>")
                            print('</td></tr>')
                    print('</table>')
                else:
                    print(f"<h2>DNS FAIL!!!</h2><p><b>{domain} not resolved.</b></p>")

            if p_check_http:
                # check http
                rc = check_http(domain, 80)
                if rc['status'] == 'ok':
                    rc_url = rc['url']
                    print(f"<h2>HTTP Success!</h2><p><b>URL: {rc_url}</b></p>")
                else:
                    rc_time = rc['time_error']
                    if 'status_code' in rc:
                        rc_code = f"Status: {rc['status_code']}"
                    else:
                        rc_code = ""
                    if 'error' in rc:
                        rc_error = f"Error: {rc['error']}"
                    else:
                        rc_error = ""
                    print(f"<h2>HTTP FAIL!!!</h2><p><b>{rc_code}<br/>{rc_error}</b></p>")

            if p_check_https:
                # check https
                rc = check_http(domain, 443)
                if rc['status'] == 'ok':
                    rc_url = rc['url']
                    print(f"<h2>HTTPS Success!</h2><p><b>URL: {rc_url}</b></p>")
                else:
                    rc_time = rc['time_error']
                    if 'status_code' in rc:
                        rc_code = f"Status: {rc['status_code']}"
                    else:
                        rc_code = ""
                    if 'error' in rc:
                        rc_error = f"Error: {rc['error']}"
                    else:
                        rc_error = ""
                    print(f"<h2>HTTPS FAIL!!!</h2><p><b>{rc_code}<br/>{rc_error}</b></p>")
    else :
        print("<p>Доменне ім'я не задано</p>")


    print("""
</div>
</body>
</html>""")
