#!/usr/bin/python3

import time
import psutil
import json
import os

print(time.localtime())
'''
def load_avg():
    f = os.popen("uptime")
    a = f.read().strip()
    return (a[a.find("average:") + 8:]).strip()


JSON = {}
log = {}
while True:
    JSON.clear()
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
    network = psutil.net_io_counters(False)
    time.sleep(1)
    network2 = psutil.net_io_counters(False)

    JSON['network']['up'] = (network2.bytes_sent - network.bytes_sent) / 1024
    JSON['network']['down'] = (network2.bytes_recv - network.bytes_recv) / 1024

    #单位为KB
    Time = time.localtime()
    JSON['time'] = time.strftime("%Y-%m-%d %H:%M:%S", Time)
    with open("/usr/share/nginx/html/info.json", 'w+') as speed:
        speed.write("CallBack(" + json.dumps(JSON) + ")")
        speed.close()
    print(JSON)
    
    if (time_)[4] % 5 == 0:
        
        with open("./" + time.strftime("%m-%d %H:%M:%S",time.localtime() + ".json"),"w+") as file:
            print(file.read())
            print(file.write("12d4as85d4as6d4as65das"))
    print("done")
    time.sleep(9)

'''