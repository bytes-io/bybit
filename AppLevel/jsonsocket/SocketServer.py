#!/usr/bin/python

# Import socket
from jsonsocket import Server
from ClientThread import ClientThread

host = ''
port = 7878 
server = Server(host, port)


server.accept()
data = server.recv()
print data
server.send({'data': [123, 456]})
server.close()

'''
# threaded
while True:
	# Establish connection with client
	server.accept()   
	print 'Got connection from', server.client_addr
	thread=ClientThread(server.client)
	thread.run()
'''



