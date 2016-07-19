from bitcoin import *
import jsonConn
'''
Some helper functions for implementation the transaction protocol:
+ exchange_Kp(ownKey, connection)
+ balanceAddr(address)
+ feeCalculator(ins, urgent=0)
+ makePtx(script, uKeyClient, uKeyServer, toServer)
+ makeDtx(rKeyClient, uKeyServer, dep)
'''

#NTS: THE WHOLE SCRIPT SIMPLIFIES THE SIGNING OF TXs BC IT ASSUMES ONLY 1 INPUT

'''
# Test
if __name__ == "__main__":
	# > DEPOSIT
	# private key of client
	rKeyClient = 'L4bZoyNLpAqXPSBKSJ157hVH69pdqMBqzckqPNofyYMFndfkrZCR'
	# public key of server
	uKeyServer = '022215c72724cfb7d7de6a16be5eec1329202fc9a80668e82cb09b02e2af541c4b'
	# deposit amount
	dep = 150000
	# building the Dtx
	[Dtx, script]  = makeDtx(rKeyClient, uKeyServer, dep)
	# sign and push Dtx
	DtxS = sign(Dtx, 0, rKeyClient)
	pushtx(DtxS)

#How does the Server verify? He verifies by having created the same script on
#his side (which demands that he has the client's public key) and checks the
#history(scriptAddr) to see if some money arrived

	scriptAddr = scriptaddr(script)
	# After the transaction:
	print("What remains in original address:")
	print balanceAddr(privkey_to_address(addrClient))
	print("The DEPOSIT address: ")
	print scriptAddr
	print("The DEPOSIT address has the follwoing tx history: ")
	print history(scriptAddr)

	# > PAYMENT
	# Params
	# arg3 - client's public key:
	uKeyClient =privtopub(rKeyClient)
	# arg4 - amount:
	toServer = 25000
	# Build PTx
	Ptx=makePtx(script, uKeyClient, uKeyServer, toServer):
	# Sign
	clientSig = multisign(Ptx, 0, script, rKeyClient)
# This works and will work, without needing a loop as opposed to what is done at http://bitscavenger.blogspot.co.uk/2014/04/multisig-with-pybitcointools.html because the PAYMENT address is funded all at once and never more than once.


	# > INTERACT WITH SERVER. We need to:

	# send the Original Raw Transaction: tx
	# (send the redemption Script: script (in fact he already has this))
	# the Signature for each input: clientSig

# Server will want to check that tx is what it ought to be (amount, beneficiary), and that clientSig is valid.

# After these checks are performed, the Server generates serverSig, and applies [serverSig, clientSig] as follows:
	serverSig = multisign(Ptx,0,script,rKeyServer)
	signedPayment = apply_multisignatures(Ptx, 0, script, clientSig, serverSig)
	pushtx(signedPayment)
#should be sigClient sigServer ....
'''


###############################################################################



# signs all inputs of a tx
def signAllIns(aTx, priv, nbIns=None):
	signedTx = aTx
	utxo = nbIns

	if utxo == None:
		utxo = len(unspent(privtoaddr(priv)))

	for i in range(utxo):
		signedTx = sign(signedTx, i, priv)
	return signedTx

# > PAYMENT

# This function takes 4 parameters makes a transcation that splits up a DEPOSIT
# designated by a script (arg1), into two public keys/addresses (arg2,3) giving
# amount arg4 to arg2 and the rest, minus a fee, to arg3.
# Returns tx

def makePtx(script, uKeyClient, uKeyServer, toServer):
	addrServer = pubtoaddr(uKeyServer)
	addrClient = pubtoaddr(uKeyClient)
	outs = [{'value':toServer, 'address':addrServer}]
	histScript = history(scriptaddr(script))
	tx = mksend(histScript, outs, addrClient, feeCalculator(histScript))
	return tx


# DEPOSIT

# This function takes 3 parameters and set up a DEPOSIT controlled by the
# holders of the private key corresponding to each of the first two parameters
# of amount arg3.
# It returns [depositTx, script]

def expressTx(anAddr, aDst, amnt):
	outs = [{'value': amnt, 'address' : aDst}]
	return mksend(unspent(anAddr), outs, anAddr, 15000)

def expressStx(aPriv, aDst, amnt):
	src = privtoaddr(aPriv)
	tx = expressTx(src, aDst, amnt)
	return signAllIns(tx, aPriv, len(unspent(src)))

def makeDtx(rKeyClient, uKeyServer, dep):
	addrClient = privkey_to_address(rKeyClient)
	utxoClient = unspent(addrClient)

	# Create Script
	pubs = []
	pubs.append(privtopub(rKeyClient))
	pubs.append(uKeyServer)
	script = mk_multisig_script(pubs[0],pubs[1],2,2)  # keys, req, total
	depositAddr = scriptaddr(script)
	histDeposit = history(depositAddr)
	if histDeposit != []:
		print 'Problem with depositAddr: non-void history.'

	# Prepare the DEPOSIT transaction
	outs = [{'value':dep, 'address':depositAddr}]
	tx = mksend(utxoClient, outs, addrClient, feeCalculator(utxoClient))

	# Return
	return [tx, script]

def setTimelock(aTx,locktime):
	dTx=deserialize(aTx)
	dTx['locktime'] = locktime
	return serialize(dtx)

# Public key exchange
def exchangePubKey(ownKey, connection):
	print "Public key exchange"
	connection.jsend(ownKey)
	out = connection.jrecv()
	return out

# Available balance of an address
def balanceAddr(address):
        avlb = sum(multiaccess(unspent(address),'value'))
        return avlb

# Optimal fee for given inputs  (arg1) and urgency level (arg2) in 1-3
def feeCalculator(ins, urgent=0):
	if urgent==1:
		return 40000
	return 14000
	# get size in bytes
	# multiply this by current price per byte from https://bitcoinfees.21.co/#delay corresponding to the level of urgency. use curl here. Firewall should allow it.
	# instead of multoplying (this multiplicative perhaps does not reflect the mining market works), estimate function
	# return fee

# Returns a selection of pas transcations to be used to fund a transfer of amount arg2, from the entire history of an address (arg1)
# def inputSelector(address, amount):
#	history = bitcoin.unspent(fromAddress)
#	totalSend = amount+fee
# Indeed wirting such a function is necessary because it permits making a shorter transaction and thus lower the fee. Bterin's library does not trim down inputs in any way. But this can be done last. A summary of the algorithms used is given at: http://bitcoin.stackexchange.com/questions/1077/what-is-the-coin-selection-algorithm?rq=1
