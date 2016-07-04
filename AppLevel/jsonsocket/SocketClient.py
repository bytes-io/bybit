#!/usr/bin/python           # This is client.py file

from jsonsocket import Client

host = '192.168.12.1' 	   
port = 7878                # Reserve a port for your service.
client = Client()
print 'Client starts.'

client.connect((host, port))
print 'Client connected.'

client.send({'tx_id': 1234, 'amount': 4321})
response = client.recv()
print response
client.close()
