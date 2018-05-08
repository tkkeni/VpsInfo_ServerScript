#!/usr/bin/python3.6


import psutil
import json
import os
import asyncio


class VpsStatus:
    networkIO = [0,0] #down,up
    hardwareInfo = {}
    shutdown = False

    def __init__(self):
        print(1)

    def hardware_info(self):
        while not self.shutdown:
            mem = psutil.virtual_memory()
            self.hardwareInfo["CPU"] = str(psutil.cpu_percent(1))
            self.hardwareInfo['load'] = self.__load_avg()

            self.hardwareInfo['mem'] = {}
            self.hardwareInfo['mem']['available'] = mem.available / 1048576
            self.hardwareInfo['mem']['total'] = mem.total / 1048576

            swap = psutil.swap_memory()
            self.hardwareInfo['swap'] = {}
            self.hardwareInfo['swap']['used'] = swap.used / 1048576
            self.hardwareInfo['swap']['total'] = swap.total / 1048576

            disk = psutil.disk_usage('/')
            self.hardwareInfo['disk'] = {}
            self.hardwareInfo['disk']['used'] = disk.used / 1048576
            self.hardwareInfo['disk']['total'] = disk.total / 1048576

            p = os.popen('vnstat --json')
            vnstat = json.loads(p.read())
            p.close()
            self.hardwareInfo['network'] = {}
            self.hardwareInfo['network']['used'] = (int(vnstat['interfaces'][0]['traffic']['total']['rx']) + int(
                vnstat['interfaces'][0]['traffic']['total']['tx'])) / 1024
            self.hardwareInfo['network']['total'] = 1000
            print("hardware_Info:", '')
            print(self.hardwareInfo)
            yield from asyncio.sleep(10)

    def network_io(self):
        while not self.shutdown:
            network = psutil.net_io_counters(False)
            yield from asyncio.sleep(1)
            network2 = psutil.net_io_counters(False)
            self.networkIO[1] = (network2.bytes_sent - network.bytes_sent) / 1024
            self.networkIO[0] = (network2.bytes_recv - network.bytes_recv) / 1024
            print("networkIO:", '')
            print(self.networkIO)

    def __load_avg(self):
        f = os.popen("uptime")
        a = f.read().strip()
        return (a[a.find("average:") + 8:]).strip()
