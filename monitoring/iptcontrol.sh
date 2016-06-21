#!/bin/bash

# Summary:
# this script encapsulates at making 5 standard IPTables manipulations. It is used by control.sh

# Usage: ./variable.sh TASKNB

# Depencies: none 

INT_IF=wlan0
EXT_IF=wlan1
IS_ALWD=217.70.184.38
MAC_CLIENT=ac:bc:32:a5:3e:ed

if [ $1 = 1 ]; then
	echo "Task 1 - Deny FORWARD by default"
	iptables -I FORWARD 1 -i $INT_IF -o $EXT_IF -j DROP # is the 'EXT_IF' necessary?
fi

if [ $1 = 2 ]; then
	echo "Task 2 - Allow free forwarding for $IS_ALWD"  
	iptables -t nat -I PREROUTING -i $INT_IF -d $IS_ALWD -j ACCEPT
	iptables -I FORWARD 1 -i $INT_IF -d $IS_ALWD -j ACCEPT
fi

if [ $1 = 3 ]; then
	echo "Task 3 - DISallow free forwarding for $IS_ALWD"  
	iptables -D FORWARD 1 
fi

if [ $1 = 4 ]; then
	echo "Task 4 -Allow client to connect (authentified by MAC address)"
	iptables -t nat -I PREROUTING -m mac --mac-source $MAC_CLIENT -j ACCEPT
	iptables -I FORWARD 2 -m mac --mac-source $MAC_CLIENT -j ACCEPT
fi

if [ $1 = 5 ]; then
	echo "Task 5 -DISallow client to connect (authentified by MAC address)"
	iptables -D FORWARD 2
fi
