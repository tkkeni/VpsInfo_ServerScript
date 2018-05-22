#!/usr/bin/python3.6


import psutil
import json
import os
import asyncio
import re
import time
import pymysql

class VpsStatus:
    networkIO = [0,0] #down,up
    performance = {}
    shutdown = False

    def __init__(self):
        print(1)

    def Ping(self):
        while time.localtime()[4]%5 != 0:
            yield from asyncio.sleep(1)
        os.popen('ping ping.warming.site -c 300 -W 1')
        output_os = os.read()
        result = re.search(r'mdev = ([0-9].*)/([0-9].*)/([0-9].*)/', output_os)
        if result:
            avg_Ping = result.group(2).strip()
        else:
            avg_Ping = 'Nan'
        result = re.search(r'received,(.*?)packet', output_os)
        if result:
            loss = result.group(1).strip()
        else:
            loss = 'Nan'


    def database_update(self):


    def hardware_info(self):
        while not self.shutdown:
            mem = psutil.virtual_memory()
            self.performance["CPU"] = str(psutil.cpu_percent(1))
            self.performance['load'] = self.__load_avg()

            self.performance['mem'] = {}
            self.performance['mem']['available'] = mem.available / 1048576
            self.performance['mem']['total'] = mem.total / 1048576

            swap = psutil.swap_memory()
            self.performance['swap'] = {}
            self.performance['swap']['used'] = swap.used / 1048576
            self.performance['swap']['total'] = swap.total / 1048576

            disk = psutil.disk_usage('/')
            self.performance['disk'] = {}
            self.performance['disk']['used'] = disk.used / 1048576
            self.performance['disk']['total'] = disk.total / 1048576

            p = os.popen('vnstat --json')
            vnstat = json.loads(p.read())
            p.close()
            self.performance['network'] = {}
            self.performance['network']['used'] = (int(vnstat['interfaces'][0]['traffic']['total']['rx']) + int(
                vnstat['interfaces'][0]['traffic']['total']['tx'])) / 1024
            self.performance['network']['total'] = 1000
            print("hardware_Info:", '')
            print(self.performance)
            yield from asyncio.sleep(10)

    def network_io(self):
        while not self.shutdown:
            network = psutil.net_io_counters(False)
            yield from asyncio.sleep(1)
            network2 = psutil.net_io_counters(False)
            self.networkIO[1] = (network2.bytes_sent - network.bytes_sent) / 1024
            self.networkIO[0] = (network2.bytes_recv - network.bytes_recv) / 1024


    def __load_avg(self):
        f = os.popen("uptime")
        a = f.read().strip()
        f.close()
        return (a[a.find("average:") + 8:]).strip()

