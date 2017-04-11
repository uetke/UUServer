"""
    instserver.beagle_bone
    ----------------------
    Simple example of how to run on a beaglebone
"""

import Adafruit_BBIO.GPIO as GPIO
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

        return True

if __name__ == '__main__':
    d = BeagleBone()
    d.blink(5)