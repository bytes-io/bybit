
from bitcoin import *
from txHelpers import *

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



#=============================================================================#

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

def makeDtx(rKeyClient, uKeyServer, dep):
	addrClient = privkey_to_address(rKeyClient)
	histClient = history(addrClient)

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
	tx = mksend(histClient, outs, addrClient, feeCalculator(histClient))	
	
	# Return
	return [tx, script]






################################################################################




