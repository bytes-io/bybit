#!/usr/bin/python
import socket

MSGLEN=65536

class MySocket(socket.socket):
	def accept(self):
		sock, a


 def accept(self):
        sock, addr = self._sock.accept()
        return _socketobject(_sock=sock), addr
    accept.__doc__ = _realsocket.accept.__doc__ 



   def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myrecv(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

'''
demonstration class only
      - coded for clarity, not efficiency

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
'''
