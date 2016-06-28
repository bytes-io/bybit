#!/usr/bin/python

# Import socket
import socket
import clientThread
# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
port = 7878                		 # Reserve a port for your service.
serversocket.bind(('', port))      		 # Bind
serversocket.listen(5)

# host

while True:
	# Establish connection with client
	c, addr = serversocket.accept()    # addr: addresse + port du client
	print 'Got connection from', addr
	ct=clientThread.ClientThread(c)
	ct.run()

'''
    count=c.send('ThankThankThankThankThankThankThankThankThankThankThank you for connecting')
    print count
    count=c.send('')
    print count
    c.send('hahaha')
    c.close()                         # Close the connection
'''
'''
    ct = ClientThread(c)
    ct.run()
'''
