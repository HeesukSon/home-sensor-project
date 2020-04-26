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
import pickle

# DEFAULT Values for conf. setting
hub_sn = 540054
sound1_port = 0
sound2_port = 1
light_port = 5
temp_port = 4
hum_port = 3
motion_port = 5
srv_ip = ''

# conf. setting loaded
with open("config.json") as json_data:
        conf = json.load(json_data)
        hub_sn = int(conf["hub_sn"])
        sound1_port = int(conf["sound1_port"])
        sound2_port = int(conf["sound2_port"])
        light_port = int(conf["light_port"])
        hum_port = int(conf["hum_port"])
        temp_port = int(conf["temp_port"])
        motion_port = int(conf["motion_port"])
        srv_ip = conf["server_ip"]

waitT = 10000
PORT = 10000

def main():
        # open Phidget channels
        snd1 = SoundSensor()
        snd2 = SoundSensor()
        temp = VoltageRatioInput()
        hum = VoltageRatioInput()
        light = VoltageInput()
        motion = VoltageInput()

        openChannels(snd1, snd2, temp, hum, light, motion)
        # Create a TCP/IP socket

        # send sensed data to db server
        #for i in range(1000):    
        while(True):
                try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server_address = (srv_ip, PORT)
                        sock.connect(server_address)
                        time.sleep(0.1)
                        sensor_data = getJSONSensorValues(snd1, snd2, temp, hum, light, motion)
                        sock.sendall(pickle.dumps(sensor_data))
                        print('Sensor data has been sent: {}'.format(sensor_data))
                except Exception as e:
                        print("Exception found: {}".format(type(e)))
                finally:
                        sock.close()
                        print('Socket has been closed.')
                time.sleep(1)
        

        # close Phidget channels
        snd1.close()
        snd2.close()
        temp.close()
        hum.close()
        light.close()
        motion.close()

def getJSONSensorValues(snd1, snd2, temp, hum, light, motion):
        data = {
                "From":getIPAddress(),
                "At":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "Sound1":snd1.getOctaves(),
                "Sound2":snd2.getOctaves(),
                "Temperature":temp.getSensorValue(),
                "Humidity":hum.getSensorValue(),
                "Light":light.getSensorValue(),
                "Motion":motion.getSensorValue()
        }
        data = json.dumps(data)
        return data

def getIPAddress():
        return str([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
        if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
        s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) 
        if l][0][0])

def openChannels(snd1, snd2, temp, hum, light, motion):
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

        motion.setDeviceSerialNumber(hub_sn)
        motion.setHubPort(motion_port)
        motion.setIsHubPortDevice(True)

        snd1.openWaitForAttachment(waitT)
        snd2.openWaitForAttachment(waitT)
        temp.openWaitForAttachment(waitT)
        hum.openWaitForAttachment(waitT)
        light.openWaitForAttachment(waitT)
        motion.openWaitForAttachment(waitT)

        temp.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_TEMPERATURE)
        hum.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_HUMIDITY)
        light.setSensorType(VoltageSensorType.SENSOR_TYPE_1127)
        motion.setSensorType(VoltageSensorType.SENSOR_TYPE_VOLTAGE)

def plotOct(octaves):
        oct_range = np.array(['31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k'])
        oct_values = np.array([round(x) for x in octaves])

        fig = tpl.figure()
        fig.barh(oct_values, oct_range, force_ascii=True)
        fig.show()
        print('')

main()
