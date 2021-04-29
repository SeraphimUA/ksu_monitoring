from random import randint
from os import getcwd, path, makedirs
from datetime import datetime, timedelta

now = datetime.now()
yesterday = now - timedelta(days=1)
# time_check = now.strftime('Date(%Y,%m,%d,%H,%M)')
time_check = f"Date({now.year},{now.month-1},{now.day},{now.hour},{now.minute})"
time_yesterday = f"Date({yesterday.year},{yesterday.month-1},{yesterday.day},{yesterday.hour},{yesterday.minute})"

with open('charts_data/kspu.edu.http.data', 'w') as f2:
    t0 = time_yesterday
    while t0 <= now:
        time_check = f"Date({t0.year},{t0.month-1},{t0.day},{t0.hour},{t0.minute})"
        f2.write(f"{time_check} {randint(0, 1)} {randint(3000, 5000)}\n")
        t0 += timedelta(minutes=5)