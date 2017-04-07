"""
client.py
=========
Client class that handles the communication with the server. It is mainly for showing how to implement a general class that works with pickle and json.

The code to run this class is::

   from instserver.client import InstClient
   # First instantiate the client with the IP address and port of the server
   c = InstClient('http://127.0.0.1:5000')
   # Let's print a list of the available devices and methods on the server
   print(c.listdevices())
   
.. sectionauthor:: Aquiles Carattino <aquiles@aquicarattino.com>
"""

import requests
import json
from instserver.messages import messages
import pickle


class InstClient(object):
    """
    Client class for communicating with a server.
    """
    def __init__(self, addr):
        """
        Client class for handling the communication with the server. It is not completely necessary, since the communication can be directly addressed with the use of requests.
        :param addr: the http address where the server is running, including the port.
        """
        self.addr = addr

    def trigger(self, name, method, arguments=None):
        """
        Triggers a remote instrument by passing its name, method and arguments
        :param name: name of the device, as registered in the server
        :param method: method to be run on the server
        :param arguments: arguments to be passed to the method
        :return: Message from the server translated according to the dictionary messages
        """
        d = json.dumps({'name': name, 'method': method, 'arguments': arguments})
        r = requests.post(self.addr+"/Trigger", data=d)
        r = json.loads(r.text)

        # Translate to the proper message
        return messages[r['Message']]

    def get(self, name, method):
        """
        Downloads data from the server
        :param name: Name of the method
        :param method: Method to get data from
        :return: whatever type of data was generated in the server
        """
        r = requests.get(self.addr+"/Read", params={'name': name, 'method': method})
        return pickle.loads(r.content)

    def listdevices(self):
        """
        Lists the devices available in the server with their methods
        :return: dictionary of devices and available methods
        """
        r = requests.get(self.addr + "/List")
        return json.loads(r.text)

if __name__ == '__main__':

    c = InstClient('http://127.0.0.1:5000')
    print(c.listdevices())
    print(c.trigger('d', 'idn'))
    input()
    print(c.trigger('d', 'measure', 2000))
    print(c.get('d', 'idn'))
    input()
    print(c.get('d', 'measure'))