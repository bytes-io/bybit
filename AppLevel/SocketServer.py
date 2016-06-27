#!/usr/bin/python

# Import socket
import socket
from mySocket import *
# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
port = 7878                		 # Reserve a port for your service.
serversocket.bind(('', port))      		 # Bind
serversocket.listen(5)

# host

while True:
	# Establish connection with client
    c, addr = serversocket.accept()
	# do sth with is
    print 'Got connection from', addr

    c.send('Thank you for connecting')
    c.send('hahaha')
    c.close()                         # Close the connection
'''
    ct = client_thread(c)
    ct.run()
'''
