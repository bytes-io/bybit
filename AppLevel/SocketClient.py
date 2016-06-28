#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create a socket object. AF_INET: address internet, SOCK_STREAM: protocole TCP
host = '192.168.12.1' # Get local machine name
port = 7878                # Reserve a port for your service.
print 'hallo'
s.connect((host, port))
print 'connected'
print s.recv(32)
print s.recv(32)

print 'great'
print s.recv(1024)

s.close()                     # Close the socket when done

'''
# question: quel est le role de l argument dans recv
Cote serveur:

msg_recu = b""
while msg_recu != b"fin":
    msg_recu = connexion_avec_client.recv(1024)
    # L'instruction ci-dessous peut lever une exception si le message
    # Réceptionné comporte des accents
    print(msg_recu.decode())
    connexion_avec_client.send(b"5 / 5")

select ou threads?
Le module select peut être utile si l'on souhaite créer un serveur pouvant gérer plusieurs connexions simultanément ; toutefois, il en existe d'autres.

    '''
