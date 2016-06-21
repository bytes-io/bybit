#!/bin/bash 

#Every 2 seconds, show:
# wlan0 RXBYTES:   TXBYTES:    |
# wlan1 RXBYTES:   TXBYTES:    |
# ******************************
#command1=`ifconfig wlan0 | grep "RX bytes"`
#command2=`ifconfig wlan1 | grep "RX bytes"`

RX1=/sys/class/net/wlan1/statistics/rx_bytes
RX0=/sys/class/net/wlan0/statistics/rx_bytes

if [ $1 -lt 80 ]; then
	echo "Data usage is shown every $1 seconds"
	initRX0=`cat $RX0`
	initRX1=`cat $RX1`
	
while [ 1 = 1 ]; do
	echo "WLAN0 (client's consumption):"
	currentRX0=`cat $RX0`
	let "diffRX0 = currentRX0 - initRX0"
	echo $diffRX0
	echo "WLAN1 (client + iisp):"
	currentRX1=`cat $RX1`
	let "diffRX1 = currentRX1 - initRX1"
	echo $diffRX1
	echo "*****************************"
	sleep $1
done

fi



# Every 250Kb (min freq is 1 sec), show:
# wlan0 RXBYTES:   TXBYTES:    |
# ******************************

if [ $1 -ge 80]; then
	echo "Data usage is shown every $1 KBytes"
while [ 1 = 1 ]; do
	echo "WLAN0:                             |"
	echo "WLAN1 (internet):                  |"
	echo "************************************"
	sleep 1
done
 
fi



