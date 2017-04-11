"""
    instserver.beagle_bone
    ----------------------
    Simple example of how to run on a beaglebone
"""

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

from time import sleep

class BeagleBone(object):
    def __init__(self):
        self.name = 'Beagle'

    def blink(self, times):
        """Blinks the LEDs for a specified number of times"""

        GPIO.setup('USR3', GPIO.OUT)

        for i in range(times):
            GPIO.output('USR3', GPIO.HIGH)
            sleep(1)
            GPIO.output('USR3', GPIO.LOW)
            sleep(1)

        return True

    def get_analog(self, port):
        """ Reads an analog signal from the beagle board
    
        :param port: string identifying the port, for example "P9_40"
        :return: value of the signal
        """
        value = ADC.read(port)

if __name__ == '__main__':
    d = BeagleBone()
    d.blink(5)
    d.get_analog("P9_40")