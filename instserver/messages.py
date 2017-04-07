"""
Dictionary to keep track of the messages passed from the server to the client. This is useful to catch errors and handle them.

The current version is only a sketch that has to be further developed. 

.. sectionauthor:: Aquiles Carattino <aquiles@aquicarattino.com>
"""

messages = {0: 'OK',
            1: 'Invalid Method',
            2: 'Device not registered in the server',
            3: 'Same thread already running'}