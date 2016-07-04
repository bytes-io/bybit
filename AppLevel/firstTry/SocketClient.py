#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = '192.168.12.1' # Get local machine name
port = 7878                # Reserve a port for your service.
print 'hallo'
s.connect((host, port))
print 'connected'
print s.recv(1024)
print 'great'
print s.recv(1024)

s.close                     # Close the socket when done
