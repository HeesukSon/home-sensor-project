from Phidget22.Devices.SoundSensor import *
from Phidget22.Devices.VoltageRatioInput import *
import termplotlib as tpl
import numpy as np
import time

hub_sn = 540054
sound1_port = 0
sound2_port = 1
light_port = 5
temp_port = 4
hum_port = 3

waitT = 5000

def main():
        snd1 = SoundSensor()
        snd1.setDeviceSerialNumber(hub_sn)
        snd1.setHubPort(sound1_port)

        snd2 = SoundSensor()
        snd2.setDeviceSerialNumber(hub_sn)
        snd2.setHubPort(sound2_port)

        temp = VoltageRatioInput()
        temp.setDeviceSerialNumber(hub_sn)
        temp.setHubPort(temp_port)

        hum = VoltageRatioInput()
        hum.setDeviceSerialNumber(hub_sn)
        hum.setHubPort(hum_port)

        snd1.openWaitForAttachment(waitT)
        snd2.openWaitForAttachment(waitT)
        temp.openWaitForAttachment(waitT)
        hum.openWaitForAttachment(waitT)

        temp.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_TEMPERATURE)
        hum.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_HUMIDITY)

        for i in range(10):
                print("Sound1 Level: {} dB".format(snd1.getdB()))
                print("Sound2 Level: {} dB".format(snd2.getdB()))
                print("Temperature: {}".format(temp.getSensorValue()))
                print("Humidity: {}".format(hum.getSensorValue()))
                #plot(snd1.getOctaves())
                time.sleep(1)

        snd1.close()

def plot(octaves):
        oct_range = np.array(['31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k'])
        oct_values = np.array([round(x) for x in octaves])

        fig = tpl.figure()
        fig.barh(oct_values, oct_range, force_ascii=True)
        fig.show()
        print('')

# call main()
main()
