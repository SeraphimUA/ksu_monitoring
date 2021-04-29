from random import randint
from os import getcwd, path, makedirs
from datetime import datetime, timedelta

now = datetime.now()
time_check = now.strftime('Date(%Y,%m,%d,%H,%M)')
time_yesterday = now - timedelta(days=1)

with open('charts_data/kspu.edu.http.data', 'w') as f2:
    t0 = time_yesterday
    while t0 <= now:
        time_check = t0.strftime('Date(%Y,%m,%d,%H,%M)')
        f2.write(f"{time_check} {randint(0, 1)} {randint(3000, 5000)}\n")
        t0 += timedelta(minutes=5)