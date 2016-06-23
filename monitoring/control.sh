#!/bin/bash 

# Summary:
# IISP side script that allows the client a certain amount of internet access (in bytes). Checks # every 5 millisecond what the current consumption of the client amounts to. Disables forwarding # in IPTables once this consumptions exceeds the value given as argument to this script.

# Usage: control.sh X  
# where X is the number of bytes to authorise

# Dependencies:
# This script uses iptcontrol.sh. 
# can deal several mac addresses using listReader.sh

#TX0=/sys/class/net/wlan0/statistics/tx_bytes
TX0=/sys/class/net/ap0/statistics/tx_bytes

initTX0=`cat $TX0`
 	
./iptcontrol.sh 4 

while [ 1 = 1 ]; do
# approach 1 - check consumption PER INTERFACE
	echo "WLAN0/AP0 (client's consumption):"
	currentTX0=`cat $TX0`
	let "diffTX0 = currentTX0 - initTX0"
	echo $diffTX0	

	echo "*****************************"

	if [ $diffTX0 -ge $1 ]; then
		echo "Data allowance is used up."
		# disallow by taking permission out of FORWARD TABLE:
		./iptcontrol.sh 5
		break		
	fi

	sleep 0.000005    # measurement intervals
done

#set Counters
#iptables -A FORWARD -o $EXT_IF -d $IPClient
#iptables -A FORWARD -i $EXT_IF -d $IPClient
#check Counters (need to parse)
#iptables -L -v
#watch --interval 0 'iptables -nvL | grep -v "0     0"'
