"""
server.py
==========

The server is the core of the package and therefore has to be the first place to look for errors or improvements. The 
server is built on top of Flask, a lightweight framework that allows to rapidly build and deploy solutions. The server 
will open a connection on a specified port on a specified listening IP address. Care has to be taken to have the port 
open on the computer, check the firewall rules if errors happen. 
 
The code to run the server should be similar to::
 
    from instserver.server import InstServer
    from instserver.dummyDevice import dummyDevice
    # First instantiate the device
    dev = dummyDevice()
    
    # Now is time for the server:
    server = InstServer(__name__)
    server.add_device(dev,'dev')
    server.run(debug=True)

.. sectionauthor:: Aquiles Carattino <aquiles@aquicarattino.com>
"""

import flask
import json
import pickle
from flask import request
from threading import Thread


class InstServer(flask.Flask):
    """
    Server class to run tasks over the network. It allows to load devices instantiated and to trigger their methods. 
    The task after triggering happens in a separate thread, meaning the several tasks can be executed concurrently. 
    """
    def __init__(self, import_name):
        flask.Flask.__init__(self,import_name)
        self.devices = {}  # Dictionary to store the devices loaded to the server
        self.running = {}  # Dictionary to store if the devices are running
        self.availableData = {}  # Dictionary to store the available data to be downloaded by the user
        self.devthreads = {}  # Dictionary of threads running

        self.route("/")(self.mainpage)
        self.route("/Devices/<name>")(self.main_device)
        self.route("/Trigger", methods=['POST', ])(self.trigger_device)
        self.route("/Read", methods=['POST', 'GET'])(self.get_data)
        self.route("/List")(self.list_devices)

    def mainpage(self):
        """ Results in a message if one checks that the server is running.
        
        :return: 
        """
        return "The server is up and running"

    def add_device(self, device, name):
        """ Registers a new device into the server class
        
        :param device: device previously initiated.
        :param name: name of the device to be used for identification.
        :return: dictionary of devices
        """
        if name in self.devices:
            raise Warning('Device with tha name already exists')
        else:
            self.devices[name] = device
            self.running[name] = False

        return self.devices

    def main_device(self, name):
        """ Returns the methods of the device. It is mostly for debugging options, since it outputs text readable from a web explorer.
        
        :param name: name of the device
        :return: methods
        """
        if name in self.devices:
            out = "Main page of device %s" % name
            out+=str([method for method in dir(self.devices[name]) if
                      callable(getattr(self.devices[name], method)) and method[0] != '_'])
            return out
        else:
            return "Device not found, please register it with add_device"

    def trigger_device(self):
        """ Triggers a specific method of a device with arguments. The device is identified by its name when registered into the server.
        Makes a connection of the signal of the thread to a function that registers the completion of the task.
        
        :return: json dump of a message
        """
        if request.method == 'POST':
            data = json.loads(request.data)
            name = data['name']
            if name in self.devices:
                dev = self.devices[name]
                method = data['method']
                m = getattr(dev, method)  # Check if the method exists
                if callable(m):
                    if name in self.devthreads:
                        if self.devthreads[name].is_alive():
                            return json.dumps({'Message': 3})
                    self.devthreads[name] = Thread(target=self.deviceThread, args=(self.devices[name], name, method, data['arguments']))
                    self.running[name] = True
                    self.devthreads[name].start()
                    return json.dumps({'Message': 0})
                else:
                    return json.dumps({'Message': 1})
            else:
                return json.dumps({'Message': 2})

    def deviceThread(self, device, name, method, args=None):
        """ Function to be run in a separate thread to trigger a mesaurement or an action on a device. It relies on the threading capabilities of Python, therefore is not running in a different core but on a different interpreter. Heavy load activities on the computer side will affect performance.
        .. todo:: The way data is exchanged to the main process is highly non-recommended, since it overwrites a dictionary belonging to the main thread. It can be improved by using signaling.
        
        :param device: Device in which to trigger the action
        :param name: name given to the device when registering it
        :param method: method to trigger in the device
        :param args: arguments to pass to the method. They can be none
        :return: updates an internal variable to the class
        """
        m = getattr(device, method)
        if args is not None:
            r = m(args)
        else:
            r = m()
        self.availableData[name, method] = r
        return True

    def threadFinish(self, name, method, r):
        """
        Method to identify when a device is done with an acquisition. This is called internally by the working thread and should not be accessed from the outside of the class.
        
        :param name: Name of device running
        :param method: Method in the device running
        :param r: output of the method
        :return: 
        """
        print('Thread Done: %s' % r)
        self.running[name] = False
        self.availableData[name, method] = r
        del self.devthreads[name, method]

    def get_data(self):
        """ Gets the data from a specific method on a device if it is available. After this, the data is not destroyed.
        """
        if request.method == 'POST':
            data = json.loads(request.data)
            if 'name' in data:
                name = data['name']
                method = data['method']
        elif request.method == 'GET':
            name = request.args.get('name')
            method = request.args.get('method')

        if self.devthreads[name].is_alive():
            response = 'Device running'
        else:
            response = self.availableData[name, method]

        return pickle.dumps(response)

    def list_devices(self):
        """ Lists the devices registered
        
        :return: json dump of a dictionary
        """
        d = {}
        for dev in self.devices:
            d[dev] = [method for method in dir(self.devices[dev]) if callable(getattr(self.devices[dev], method)) and method[0] != '_']

        return json.dumps(d)

if __name__ == '__main__':
    try:
        from beagle_bone import BeagleBone
        d = BeagleBone()
    except:
        from dummyDevice import DummyDevice
        d = DummyDevice()

    server = InstServer(__name__)
    server.add_device(d, 'd')
    server.run(host='0.0.0.0', debug=True)














