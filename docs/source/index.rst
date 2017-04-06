.. Instrument Server documentation master file, created by
   sphinx-quickstart on Thu Apr  6 17:08:34 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Instrument Server and Client package
====================================

The instrument server is built on top of Flask while the client relies on the requests module. The client is not necessary, but outlines the basic communication with the server.

The server uses as inputs the devices already instantiated, meaning that one passes as arguments variables that already hold the communication with the device. This enables to pass several devices that rely on the same class. The devices are registered in an internal dictionary of the server, avoiding the possibility of triggering actions more than once.

The measurements are done in separated threads to avoid timeouts in the server and to allow the user to trigger several actions simultaneously. The thread relies on python threading capability and therefore should not be used with computer intensive operations, but with device intensive operations.

==================
How to use it
==================

You need to import the instserver package into your own project and load the devices you want to have available.

==================
Server side
==================

In the server side you run just the server and the classes that correspond to the devices. If you need more personalization, you can always check the documentation at Flask, specially regardin the listening IP and port::

   from instserver.server import InstServer
   from instserver.dummyDevice import dummyDevice
   # First instantiate the device
   dev = dummyDevice()

   # Now is time for the server:
   server = InstServer(__name__)
   server.add_device(dev,'dev')
   server.run(debug=True)

==================
Client side
==================
The code is::

   from instserver.client import InstClient
   # First instantiate the client with the IP address and port of the server
   c = InstClient('http://127.0.0.1:5000')
   # Let's print a list of the available devices and methods on the server
   print(c.listdevices())

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
