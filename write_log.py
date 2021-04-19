def write_log(filename, strn):
    with open(filename, 'a') as l:
        l.write(Monitoring.timestamp() + " " + strn + "\n")
