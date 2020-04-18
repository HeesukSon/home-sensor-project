from Phidget22.Devices.SoundSensor import *
import termplotlib as tpl
import numpy as np
import time

def main():
        ch = SoundSensor()
        ch.setDeviceSerialNumber(540054)
        ch.setHubPort(0)

        ch.openWaitForAttachment(5000)

        for i in range(10):
                print("Sound Level: {} dB".format(ch.getdB()))
                plot(ch.getOctaves())
                time.sleep(1)

        ch.close()

def plot(octaves):
        oct_range = np.array(['31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k'])
        oct_values = np.array([round(x) for x in octaves])

        fig = tpl.figure()
        fig.barh(oct_values, oct_range, force_ascii=True)
        fig.show()
        print('')

# call main()
main()
