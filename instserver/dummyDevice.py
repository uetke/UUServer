import numpy as np
from time import sleep

class dummyDevice(object):
    def __init__(self):
        self.name = 'Dummy'

    def initialize(self):
        return True

    def idn(self):
        sleep(2)
        return 'SN: 123456789'

    def measure(self, time):
        sleep(time/1000)
        return np.random.random(time)

if __name__ == '__main__':
    d = dummyDevice()
    print(d)
    f = getattr(d,'idn')
    print(f())