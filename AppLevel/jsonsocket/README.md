I found jsonsocket at https://github.com/mdebbar/jsonsocket.

Alternative implementation of JSON over TCP would be:
https://cpiekarski.com/2011/05/09/super-easy-python-json-client-server/

Problem with the projects outlined above: multithreading implies we are back to
plain sockets. A probable to do will be: design separate that takes socket as 
constructor argument but embeds send/rcvs into json optimized structures. 


jsonsocket
==========

This is a small Python library for sending data over sockets.

It allows sending lists, dictionaries, strings, etc. It can handle very large data (I've tested it with 10GB of data). Any JSON-serializable data is accepted.

Examples:

```python
from jsonsocket import Client, Server

host = 'localhost'
port = '8000'

# Client code:
client = Client()
client.connect(host, port).send({'some_list': [123, 456]})
response = client.recv()
# response now is {'data': {'some_list': [123, 456]}}
client.close()


# Server code:
server = Server(host, port)
server.accept()
data = server.recv()
# data now is: {'some_list': [123, 456]}
server.send({'data': data}).close()

```
