#!/bin/bash 

# Summary:
# IISP side script that allows the client a certain amount of internet access (in bytes). Checks # every 5 millisecond what the current consumption of the client amounts to. Disables forwarding # in IPTables once this consumptions exceeds the value given as argument to this script.

# Usage: control.sh X  
# where X is the number of bytes to authorise

# Dependencies:
# This script uses iptcontrol.sh. 

TX1=/sys/class/net/wlan1/statistics/tx_bytes
TX0=/sys/class/net/wlan0/statistics/tx_bytes

initTX0=`cat $TX0`
initTX1=`cat $TX1`
	
./iptcontrol.sh 4

while [ 1 = 1 ]; do
	echo "WLAN0 (client's consumption):"
	currentTX0=`cat $TX0`
	let "diffTX0 = currentTX0 - initTX0"
	echo $diffTX0	

#	echo "WLAN1 (client + iisp):"
#	currentRX1=`cat $RX1`
#	let "diffRX1 = currentRX1 - initRX1"
#	echo $diffRX1
	echo "*****************************"

	if [ $diffTX0 -ge $1 ]; then
		echo "Data allowance is used up."
		# disallow by taking permission out of FORWARD TABLE:
		./iptcontrol.sh 5
		break		
	fi

	sleep 0.000005    # measurement intervals
done


