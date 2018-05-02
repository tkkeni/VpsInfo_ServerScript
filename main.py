#!/usr/bin/python3

import time
import psutil
import json
import os


def load_avg():
    f = os.popen("uptime")
    a = f.read().strip()
    return (a[a.find("average:") + 8:]).strip()


JSON = {}
log = {}
while True:
    JSON.clear()
    for i in range(5):
        network = psutil.net_io_counters(False)
        time.sleep(1)
        network2 = psutil.net_io_counters(False)
        JSON['up'] = (network2.bytes_sent - network.bytes_sent) / 1024
        JSON['down'] = (network2.bytes_recv - network.bytes_recv) / 1024
        with open("networkIO.json", 'w+') as speed:#/usr/share/nginx/html/networkIO.json
            speed.write("CallBack(" + json.dumps(JSON) + ")")
        print(JSON)
        time.sleep(1)
    JSON.clear()
    mem = psutil.virtual_memory()
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
    Time = time.localtime()
    JSON['time'] = time.strftime("%Y-%m-%d %H:%M:%S", Time)
    with open("info.json", 'w+') as speed: #/usr/share/nginx/html/info.json
        speed.write("CallBack(" + json.dumps(JSON) + ")")
        speed.close()
    print(JSON)
    if Time[4] % 5 == 0:
        with open(time.strftime("%m-%d", Time) + ".json","w+") as f:
            mystr = f.read().strip('CallBack\(').strip('\)')
            print(mystr)
            if mystr == "":
                for i in range(288):
                    log[i] = {} 
            else:
                log = json.loads(mystr)
            print(log)
            del JSON['time']
            
            log[str(int((Time[3] * 60 + Time[4]) / 5))] = JSON
            f.write("CallBack(" + json.dumps(log) + ")")
