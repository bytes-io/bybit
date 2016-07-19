#!/bin/python

# standard imports:
from threading import Thread
from time import sleep
from random import randint
import socket,sys, select
import json
from pprint import *
import bitcoin
# own imports:
import jsonConn, hpUtils, txUtils


# Parameters to be, later on, inputed to the program (rather than harcoded)

class connManager(Thread):

	def __init__(self,_c, info):
		Thread.__init__(self)
		self.c = _c
		self.balance = 0
		self.usage = 0
		self.ipClient = info
		self.privS =' '
		self.lastpayment = None
		self.lastsig = None
		self.pubKeyClient = None
	def controlSpin(self):
		# testing
		while True:
			sleep(4)
			print 'Current balance: %d' %self.balance
			print 'Current usage: ',hpUtils.retrieveUsage(self.ipClient)
			if hpUtils.retrieveUsage(self.ipClient) > self.balance:
				print 'Usage exceeds balance > deny Fwd'
				self.cashier.signal=False
				hpUtils.denyFwd(self.ipClient)
				return
		# i = 0
		# while i < 8:
		# 		sleep(6)
		# 		print 'Manager control spin'
		# 		i += 1
		# self.cashier.signal = False

	def notify(self, payment, signature):
		self.balance += 50000
		self.lastpayment  = payment
		self.lastsig = signature

	def pushPayment(self):
		compliantScript = bitcoin.mk_multisig_script([bitcoin.privtopub(self.privS), self.pubKeyClient], 2,2)  # inversion!!!!
		sigServer = bitcoin.multisign(self.lastpayment, 0, compliantScript, self.privS)
		signedPtx = bitcoin.apply_multisignatures(self.lastpayment, 0, compliantScript, [self.lastsig, sigServer])
		print 'Broadcast the very last payment. Just got richer. Tx hash:', bitcoin.txhash(signedPtx)
		bitcoin.pushtx(signedPtx)

	def run(self):
		print 'Initialisation of MPC...'

		# exchange public keys
		pubKeyServer = bitcoin.privtopub(self.privS)
		print 'pubKeyServer: ', pubKeyServer
		self.pubKeyClient = txUtils.exchangePubKey(pubKeyServer, self.c)
		print '################################# Handshake ####################################'
		print 'Public Key received from client is: ', self.pubKeyClient

		# receive the signed Dtx and
		signedDtx = self.c.jrecv()
		print 'SignedDtx:' , signedDtx
		#print pprint(bitcoin.deserialize(signedDtx))
		scriptDtx = self.c.jrecv()
		print 'ScriptDtx: ',  scriptDtx
		print 'Ownscript: '
		own = bitcoin.mk_multisig_script([bitcoin.privtopub(self.privS), self.pubKeyClient], 2,2)  # inversion!!!!
		print own
		self.c.close()
		# broadcast D
		bitcoin.pushtx(signedDtx)
		print '############################### MPC initialised ################################'
		self.balance += 1000000

		# authorize use of the internet:
		hpUtils.allowFwd(self.ipClient)

		# set up Cashier (observed)
		self.cashier = cashier(self.c)
		self.cashier.addObserver(self)    # obviously not the right way
		self.cashier.start()

		# start control spin
		self.controlSpin()

		# broadcast payment
		print 'Manager broadcasts payment'
		self.pushPayment()

		# terminate cashier
		print "Manager waiting for cashier's termination"
		self.cashier.join()
		#self.c.close()

		print 'Manager terminating'

class cashier(Thread):
        def __init__(self, _c):
                Thread.__init__(self)
                self.c = _c
		self.signal = True
		self.observers = []
		self.payment = None
		self.signature = None

	def addObserver(self, obs):
		self.observers.append(obs)

	def extractAmount(self, payment):
		#d = bitcoin.deserialize(payment)
		return d['outs'][0]['value']

	def notifyObservers(self, payment, signature):
		#amnt = extractAmount(payment)
		#for obs in self.observers:obs.balance +=50000
		for obs in self.observers: obs.notify(payment, signature)

	def verifyPayment(self, payment, amount):
		# deserialized payment:
		#desPay = bitcoin.deserialize(payment)
		# verify amount
	 	#if desPay['outs'][0]['value'] < amount:
		#	print 'Wrong Amount'
		#	return False
		# verify beneficiary
		#if desPay['outs'][0]['script']
		#	return False
		if payment == None: return False
		return True

        def run(self):
		print 'Cashier running'
		self.amount = 0
		while self.signal:

			# reinit payment and sig to 0
			self.payment = None
			self.signature = None

			# init the select structure for blocking sockets
			self.rlist =[]
			self.wlist =[]
			self.xlist =[]
			self.toread=[self.c]

			# use output of select: receive payment
			# if self.rlist != []: self.payment = self.c.jrecv()
			self.rlist, self.wlist, self.xlist = select.select(self.toread, [], [], 2)
			if self.rlist != []:
				for connection in self.rlist: self.payment = connection.jrecv()

			if self.payment != None:
				print '################################################################################'
				print 'A transaction template was received:'
				pprint(self.payment)
				#print bitcoin.deserialize(self.payment)

			# receive signature
			self.toread=[self.c]
			self.rlist, self.wlist, self.xlist = select.select(self.toread, [], [], 2)
			if self.rlist != []:
				for connection in self.rlist: self.signature = connection.jrecv()

			if self.signature != None:
				print 'Signature:'
				pprint(self.signature)

			if self.verifyPayment(self.payment, 12):
				print 'Verify payment (business logic OK, format OK, crypto OK)'
				print "Update client's balance"
				self.notifyObservers(self.payment, self.signature)
			sleep(.5)

		self.c.close()
		print 'Cashier stopping'



##############################################################################
# This is the code of the dispatcher
if __name__ == "__main__":

	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 7878
	serversocket.bind(('', port))
	serversocket.listen(5)

	noConnections = 0
	# First, forbid all forwarding
	# set default policy of FORWARD to drop
	hpUtils.setChainPolicy('FORWARD','DROP')
	# flush FORWARD
	hpUtils.flushChain('FORWARD')
	# authorize interaction with blockchain.info
        hpUtils.allowSpecificWebsite('104.16.54.3')
        hpUtils.allowSpecificWebsite('104.16.55.3')

	print('Done with Iptables setup')

	# Second, connect with clients
	while True:
		c, addr = serversocket.accept()
		print 'Got connected by: ', addr
		cm = connManager(jsonConn.JsonConn(c), addr[0])
		cm.start()
		noConnections += 1

# class Dispatcher(object):
#
# 	def __init__(self,_port, ip='', _maxConnections = 5):
# 		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 		self.port = _port
# 		self.noConnections = 0
# 		self.maxConnections = _maxConnections
# 		self.serversocket.bind((ip, _port))
# 		self.serversocket.listen(5)
# 		self.signal = True
#
# 	def initIPTables(self):
# 		hpUtils.setChainPolicy('FORWARD','DROP')
# 		# flush FORWARD
# 		hpUtils.flushChain('FORWARD')
# 		# authorize interaction with blockchain.info
# 		hpUtils.allowSpecificWebsite('104.16.54.3')
# 		hpUtils.allowSpecificWebsite('104.16.55.3')
# 		print('Done with Iptables setup')
#
# 	def notifyConnectionEnd(self, notifier):
# 		self.noConnections -= 1
# 		print 'Dispatcher was signaled that a connection was ended by', notifier
#
# 	def startDispatching(self):
# 		# Second, connect with clients
# 		while self.signal:
# 			c, addr = serversocket.accept()
# 			print 'Got connected by: ', addr
# 			cm = connManager(jsonConn.JsonConn(c), addr[0])():
# 			cm.start()
# 			noConnections += 1
# 			print 'No of connection is now:', self.noConnections
#
# 		print 'Stopped dispatching'
#
#
# 	def stopDispatching(self):
# 		print 'Dispatcher was asked to stop'
# 		self.Signal = False
