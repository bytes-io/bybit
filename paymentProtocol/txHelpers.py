from bitcoin import *

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



