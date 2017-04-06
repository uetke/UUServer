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
