#!/bin/python
import socket, socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                
port = 7878                              
serversocket.bind(('', port))           
serversocket.listen(5)

while True:                                                                     
    c, addr = serversocket.accept()                                             
    cm = connManager(c)
    cm.run()

                          
