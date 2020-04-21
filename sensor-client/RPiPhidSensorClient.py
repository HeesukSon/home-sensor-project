from Phidget22.Devices.SoundSensor import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.VoltageInput import *
import termplotlib as tpl
import numpy as np
import time
import json
import socket
import socket
import sys

# DEFAULT Values - To be updated in openChannels() method
hub_sn = 540054
sound1_port = 0
sound2_port = 1
light_port = 5
temp_port = 4
hum_port = 3
srv_ip = ''

waitT = 10000

PORT = 10000

def main():
        loadConf()

        # open Phidget channels
        snd1 = SoundSensor()
        snd2 = SoundSensor()
        temp = VoltageRatioInput()
        hum = VoltageRatioInput()
        light = VoltageInput()

        openChannels(snd1, snd2, temp, hum, light)

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('192.168.87.27', PORT)
        print('connecting to {} port {}'.format(srv_ip, PORT))
        sock.connect(server_address)

        # send sensed data to db server
        try:
                #for i in range(10):
                sock.sendall(getJSONSensorValues(snd1, snd2, temp, hum, light).encode())
                time.sleep(5)
        finally:
                print('closing socket')
                sock.close()
                
        # close Phidget channels
        snd1.close()
        snd2.close()
        temp.close()
        hum.close()
        light.close()

def getJSONSensorValues(snd1, snd2, temp, hum, light):
        data = {
                "From":getIPAddress(),
                "At":time.ctime(time.time()),
                "Sound1":snd1.getOctaves(),
                "Sound2":snd2.getOctaves(),
                "Temperature":temp.getSensorValue(),
                "Humidity":hum.getSensorValue(),
                "Light":light.getSensorValue()
        }
        data = json.dumps(data)
        return data

def getIPAddress():
        return str([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
        if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
        s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) 
        if l][0][0])

def loadConf():
        with open("config.json") as json_data:
                conf = json.load(json_data)
                hub_sn = int(conf["hub_sn"])
                sound1_port = int(conf["sound1_port"])
                sound2_port = int(conf["sound2_port"])
                light_port = int(conf["light_port"])
                hum_port = int(conf["hum_port"])
                temp_port = int(conf["temp_port"])
                srv_ip = conf["server_ip"]
                print("srv_ip:{}".format(srv_ip))

def openChannels(snd1, snd2, temp, hum, light):
        snd1.setDeviceSerialNumber(hub_sn)
        snd1.setHubPort(sound1_port)

        snd2.setDeviceSerialNumber(hub_sn)
        snd2.setHubPort(sound2_port)

        temp.setDeviceSerialNumber(hub_sn)
        temp.setHubPort(temp_port)
        temp.setIsHubPortDevice(True)

        hum.setDeviceSerialNumber(hub_sn)
        hum.setHubPort(hum_port)
        hum.setIsHubPortDevice(True)

        light.setDeviceSerialNumber(hub_sn)
        light.setHubPort(light_port)
        light.setIsHubPortDevice(True)

        snd1.openWaitForAttachment(waitT)
        snd2.openWaitForAttachment(waitT)
        temp.openWaitForAttachment(waitT)
        hum.openWaitForAttachment(waitT)
        light.openWaitForAttachment(waitT)

        temp.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_TEMPERATURE)
        hum.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_HUMIDITY)
        light.setSensorType(VoltageSensorType.SENSOR_TYPE_1127)

def plotOct(octaves):
        oct_range = np.array(['31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k'])
        oct_values = np.array([round(x) for x in octaves])

        fig = tpl.figure()
        fig.barh(oct_values, oct_range, force_ascii=True)
        fig.show()
        print('')

main()
