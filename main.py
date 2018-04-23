#!/usr/bin/python3

import time
import psutil
import json
import os


def load_avg():
    f = os.popen("uptime")
    a = f.read().strip()
    return (a[a.find("average:") + 8:]).strip()


timeCount = 0
interval_speed = 1
interval_other = 10
JSON = {}

while True:
    JSON.clear()
    network = psutil.net_io_counters(False)
    time.sleep(1)
    network2 = psutil.net_io_counters(False)

    JSON['up'] = (network2.bytes_sent - network.bytes_sent) / 1024
    JSON['down'] = (network2.bytes_recv - network.bytes_recv) / 1024
    with open("/usr/share/nginx/html/speed.json", 'w+') as speed:
        speed.write("CallBack(" + json.dumps(JSON) + ")")
        speed.close()
    timeCount += 1
    if timeCount < 10:
        continue
    timeCount = 0
    mem = psutil.virtual_memory()
    JSON.clear()
    JSON['CPU'] = str(psutil.cpu_percent(1))
    JSON['load'] = load_avg()

    JSON['mem'] = {}
    JSON['mem']['available'] = mem.available / 1048576
    JSON['mem']['total'] = mem.total / 1048576

    swap = psutil.swap_memory()
    JSON['swap'] = {}
    JSON['swap']['used'] = swap.used / 1048576
    JSON['swap']['total'] = swap.total / 1048576

    disk = psutil.disk_usage('/')
    JSON['disk'] = {}
    JSON['disk']['used'] = disk.used / 1048576
    JSON['disk']['total'] = disk.total / 1048576

    p = os.popen('vnstat --json')
    vnstat = json.loads(p.read())
    p.close()
    JSON['network'] = {}
    JSON['network']['used'] = (int(vnstat['interfaces'][0]['traffic']['total']['rx']) + int(vnstat['interfaces'][0]['traffic']['total']['tx'])) / 1024
    JSON['network']['total'] = 1000
    #单位为KB
    JSON['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("/usr/share/nginx/html/info.json", 'w+') as speed:
        speed.write("CallBack(" + json.dumps(JSON) + ")")
        speed.close()
    print(JSON)

    print("done")
