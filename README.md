### Instrument Server/Client ###
The main purpose of this project is to have a server running in a remote machine, accessible via the network, that can trigger actions on devices. 

The server is built around Flask with threading for the actions on devices, allowing to concurrently trigger long measurements or processes.

More documentation is available at [uuserver.readthedocs.io](http://uuserver.readthedocs.io)

## How to use it ##

You need to import the instserver package into your own project and load the devices you want to have available. 

### Server side ###
In the server side you run just the server and the classes that correspond to the devices. If you need more personalization, you can always check the documentation at Flask, specially regardin the listening IP and port.

```python
from instserver.server import InstServer
from instserver.dummyDevice import dummyDevice
# First instantiate the device
dev = dummyDevice()

# Now is time for the server:
server = InstServer(__name__)
server.add_device(dev,'dev')
server.run(debug=True)
```

### Client side ###
```python
from instserver.client import InstClient
# First instantiate the client with the IP address and port of the server
c = InstClient('http://127.0.0.1:5000')
# Let's print a list of the available devices and methods on the server
print(c.listdevices())
```

## Building the documentation
The documentation of the program can be build locally and is available at http://uuserver.readthedocs.io/. 

To build the documentation locally, you need to have sphinx installed. Go to the folder docs and run the following command:

```python
    sphinx-build -b html source/ build/
```

This will build all the documentation from the source folder into the build folder. Remember that for it to work, the program needs to import every module, therefore you can't build the documentation if you don't have the dependencies in order.