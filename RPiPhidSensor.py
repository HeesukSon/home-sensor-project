from Phidget22.Devices.SoundSensor import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.VoltageInput import *
import termplotlib as tpl
import numpy as np
import time
import json

hub_sn = 540054
sound1_port = 0
sound2_port = 1
light_port = 5
temp_port = 4
hum_port = 3

waitT = 10000

def main():
        snd1 = SoundSensor()
        snd2 = SoundSensor()
        temp = VoltageRatioInput()
        hum = VoltageRatioInput()
        light = VoltageInput()

        openChannels(snd1, snd2, temp, hum, light)

        #for i in range(10):
        #        print("Sound1 Level: {} dB".format(snd1.getdB()))
        #        print("Sound2 Level: {} dB".format(snd2.getdB()))
        #        print("Temperature: {}".format(temp.getSensorValue()))
        #         print("Humidity: {}".format(hum.getSensorValue()))
        #        print("Precision Light: {}".format(light.getSensorValue()))
                # uncomment this line and the one below to visualize octaves values
                # plotOct(snd1.getOctaves())
        #        print('')
        #        time.sleep(1)
        for i in range(10):
                print(getJSONSensorValues(snd1, snd2, temp, hum, light))
                print('')
                time.sleep(1)

        snd1.close()
        snd2.close()
        temp.close()
        hum.close()
        light.close()

def getJSONSensorValues(snd1, snd2, temp, hum, light):
        data = {
                "Sound1":snd1.getOctaves(),
                "Sound2":snd2.getOctaves(),
                "Temperature":temp.getSensorValue(),
                "Humidity":hum.getSensorValue(),
                "Light":light.getSensorValue()
        }
        data = json.dump(data)
        return data

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
