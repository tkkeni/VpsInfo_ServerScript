import asyncio
import websockets
import VpsInfo
import json


def route_hardware_info():
    return json.dumps(vps_info.hardware_info())


def route_network_io():
    return json.dumps(vps_info.networkIO)


requestRoute = {"networkIO": route_network_io, "hardwareInfo": route_hardware_info}


async def echo(websocket, path):
    async for message in websocket:
        print(message)
        if message not in requestRoute:
            await websocket.send("request unknow")
        else:
            await websocket.send(requestRoute[message]())


vps_info = VpsInfo.VpsStatus()

tasks = [vps_info.hardware_info(),
         vps_info.network_io(),
         websockets.serve(echo, 'localhost', 8765)]
asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
asyncio.get_event_loop().run_forever()
