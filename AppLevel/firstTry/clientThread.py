import sys 
from threading import Thread 
import socket
import time

class ClientThread(Thread):
	def __init__(self, _c):
		Thread.__init__(self)
		self.c=_c
	def run(self):
		# a very short message
		short = self.c.send('Welcome')
		print short
		# a 0 byte message
		zero = self.c.send('')
		print zero
		# a very long message
		vlong = self.c.send('Welcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome GoodbyeWelcome Goodbye')
		print vlong
		time.sleep(5)
		self.c.close() 

