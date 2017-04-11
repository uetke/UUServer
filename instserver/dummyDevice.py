"""
dummyDevice.py
==============
Dummy device for testing the server and client. The dummy device defines three methods, initialize with returns True, idn that sleeps for two seconds and returns a string and measure that takes one argument and returns a numpy array after sleeping.

.. sectionauthor:: Aquiles Carattino <aquiles@aquicarattino.com>
"""

import numpy as np
from time import sleep


class dummyDevice(object):
    """Dummy Device class"""
    def __init__(self):
        self.name = 'Dummy'

    def initialize(self):
        """
        Initializes the dummy device
        :return: True
        """
        return True

    def idn(self):
        """
        Identifies the dummy device via a serial number
        :return: Serial number
        """
        sleep(2)
        return 'SN: 123456789'

    def measure(self, time):
        """
        Simulates a measurement with number of points defined by input and sleeping the same number of milliseconds.
        
        :param int time: 
        :return: random numpy array
        """
        sleep(time/1000)
        return np.random.random(time)

if __name__ == '__main__':
    d = dummyDevice()
    print(d)
    f = getattr(d,'idn')
    print(f())