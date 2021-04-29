from monitoring.net_utils import check_http
import monitoring.config_loader as cl
from os import getcwd, path, makedirs
from datetime import datetime, timedelta

# load config from file config.yaml
config = cl.load_config()

# select list of hosts
hosts = config['hosts']

# domain loop
for domain in hosts.keys():

    result = check_http(config, domain, 80)

    now = datetime.now()
    yesterday = now - timedelta(days=1)
#    time_check = now.strftime('Date(%Y,%m,%d,%H,%M)')
    time_check = f"Date({now.year},{now.month - 1},{now.day},{now.hour},{now.minute})"
    time_yesterday = f"Date({yesterday.year},{yesterday.month - 1},{yesterday.day},{yesterday.hour},{yesterday.minute})"
#    time_yesterday = (now - timedelta(days=1)).strftime('Date(%Y,%m,%d,%H,%M)')
    check_status = 1 if result['status'] == 'ok' else 0
    runtime_check = result['runtime'] if 'runtime' in result else 0

    # check if dir "results" exists. If not, make it
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
        f2.write(f"{time_check} {check_status} {runtime_check}\n")
