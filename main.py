import subprocess as sp
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
import csv
import sys

# INIT COLLECTOR
file = 'ua.csv'
data = pd.read_csv(file)
data = data.replace(np.NaN, 'N/A')
p_ip = list(data.ip_address)
p_city = list(data.city)
city = []
ip = []
service = []
service_online = []
service_offline = []

# filter NaN
for x in range(len(p_city)):
    if p_city[x] != 'N/A':
        city.append(p_city[x])
        ip.append(p_ip[x])


print('# # # CHECKING IN RANGE OF TOTAL: ' + str(len(ip)) + ' IPs # # #')

# status code 0 = success / status code 1 = failed
for x in range(len(ip)):
    # for x in range(32):
    status = sp.call(['tcping', '-c', '1', '-t', '1', str(ip[x])], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    if status == 0:
        indic = 'ONLINE'
        service.append('ONLINE')
        service_online.append(x)
    else:
        indic = 'OFFLINE'
        service.append('offline')
        service_offline.append(x)
    print('[CHECKING | ' + str(x+1) + '/' + str(len(ip)) + ']: '
          + str(ip[x]) + ' - ' + str(city[x]) + ' | Status: ' + indic)


print('[' + str(len(service_online)) + '/' + str(len(ip)) + '] SERVER ONLINE -> ' + str(len(service_offline))
      + ' SERVER OFFLINE.')


# sort both lists
city, service = zip(*sorted(zip(city, service)))


# INIT CSV
# datapath = '/scraper/data/ukr_ping1/'  # absolute path for docker-linux
datapath = 'data/ukr_ping1/'  # relative path for local testing
path = datapath + 'ukr_ping1.csv'
CSV_HEADER = ['DATETIME'] + list(city)

# create timestamp
dateTimeObj = datetime.now()
dateObj = dateTimeObj.date()
timeObj = dateTimeObj.time()
dateStr = dateObj.strftime("%Y-%m-%d")
timeStr = timeObj.strftime("%H:%M")
timestamp = [dateStr + ' ' + timeStr]
print(timestamp)

CSV_BODY = timestamp + list(service)


try:
    Path(datapath).mkdir(parents=True, exist_ok=True)  # if folders don't exist
    Path(path).touch(exist_ok=True)  # if csv don't exists
except PermissionError:
    print('Creating folder and csv-file failed. Check permissions.')
    sys.exit()

# write zeros if file is empty
csv_empty = os.stat(path).st_size == 0

if csv_empty is True:
    with open(path, 'w+', encoding='utf8', newline='') as f:
        writeZero = csv.writer(f)
        writeZero.writerow(CSV_HEADER)


# Debug lists // check if length of lists are equal
if len(CSV_HEADER) == len(CSV_BODY):
    print('[!] (Check Lists): Lists are equal.\n')
else:
    print('[!] (Check Lists) WARNING: Lists are NOT matching!\n')


# write data into csv
with open(path, 'a', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(CSV_BODY)
    print(timeStr + ' ' + dateStr + ': Data collecting successful!')

