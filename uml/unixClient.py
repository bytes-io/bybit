from bitcoin import *
from txUtils import *
from jsonConn import *
from time import sleep


	# Ptx=makePtx(script, privtopub(rKeyClient), uKeyServer, 50000)
	# clientSig = multisign(Ptx, 0, script, rKeyClient)
 # 	conn.jsend(Ptx)#
	# conn.jsend(clientSig)#



def paymentSpin(redeemScript, conn, privkeyC, pubkeyS, increment):
	amount = 0
	i = 0
	print 'inpaymentspin'
	while i<10:
		print 'Paid so far: ', amount
		amount += increment
		i+=1
		# make a payment transaction with amount += increment
		Ptx = makePtx(privtopub(privkeyC), pubkeyS, amount)
		# partially sign it
		clientSig = multisign(Ptx, 0, redeemScript, privkeyC)
		# send Ptx
		conn.jsend(Ptx)
		# send client signature
		sleep(.2)
		conn.jsend(clientSig)
		sleep(2)
	print 'Total spent this time: %d' %amount
	return amount

# Test
if __name__ == "__main__":
	if len(sys.argv) > 1:
		host = str(sys.argv[1])
	else:
		host = '192.168.12.1'

	# private key of client
	rKeyClient = 'KyLuCNsxddnqpdJW1Q3q2mQtkssThJUfcGq9hdCE8W72xYPD3He3'  # 1CA1rufdFggCkd4kZQaff6NxZa1P9AfrrE

	# connect
	conn = JsonConn()
	conn.connect((host,7879))

	# HANDSHAKE
	uKeyServer = exchangePubKey(privtopub(rKeyClient), conn)
	#uKeyServer = '029cb4cbc58ff1b71b9aee78b0228313201e09d4a3bf263ed8e7e31709e49f7d28' # 1QKb78KGXGivbgMXJbVmUz6Tp9w6BAtYve
	dep = balanceAddr(privtoaddr(rKeyClient)) - 15000
	# building the Dtx
	[Dtx, script]  = makeDtx(rKeyClient, uKeyServer, dep)
	# sign and send Dtx
	DtxS = signAllIns(Dtx, rKeyClient)
	print DtxS
	conn.jsend(DtxS) #
	conn.jsend(script)#
	sleep(3)
	# book keeping
 	scriptAddr = scriptaddr(script)
	print("What remains in original address:")
	print balanceAddr(privkey_to_address(rKeyClient))
	print("The DEPOSIT address: ")
	print scriptAddr
	print("The DEPOSIT address has the following tx history: ")
	print history(scriptAddr)

	# PAY AS YOU CONSUME
	paymentSpin(script, conn, rKeyClient, uKeyServer, 1000)

	# close the channel
	conn.close()
	print 'Internet is overrated'
