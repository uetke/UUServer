"""
instThread.py
=============
This class is not used any more but is left as an example of how it can be implemented. I like the signaling strategy of Qt, but it is not trivial to implement it with Flask. 
Looking around, I've found that Celery can be a good way for async tasks, together with blink. More research on those have to be done, since Flask already comes with some signaling interfaces.

.. sectionauthor:: Aquiles Carattino <aquiles@aquicarattino.com>
"""

from PyQt4 import QtCore


class instThread(QtCore.QThread):
    """Thread for communicating with a specific device.
    """
    threadDone = QtCore.SIGNAL('threadDone')
    def __init__(self, device, name, method, args=None):
        QtCore.QThread.__init__(self)
        self.name = name
        self.method = getattr(device, method)
        self.args = args

    def __del__(self):
        self.wait()

    def run(self):
        """ Maintains the communication with the device
        """
        if self.args is not None:
            r = self.method(self.args)
        else:
            r = self.method()

        self.emit(self.threadDone, self.name, self.method, r)
        return
