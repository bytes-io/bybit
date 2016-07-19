#!/bin/python
# see https://wiki.archlinux.org/index.php/simple_stateful_firewall
import iptc

def allowFwd(anIP):
# allows all forwarding to/by a client on the network
	# iptables -A FORWARD -s $IP_CLIENT -j ACCEPT
	chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
	rule = iptc.Rule()
	rule.src = anIP+"/255.255.255.255"
	target = iptc.Target(rule, "ACCEPT")
	rule.target = target
	chain.append_rule(rule)
	# iptables -A FORWARD -d $IP_CLIENT -j ACCEPT
	rule2 = iptc.Rule()
	rule2.dst = anIP+"/255.255.255.255"
	target2 = iptc.Target(rule2, "ACCEPT")
	rule2.target = target
	chain.append_rule(rule2)

def denyFwd(anIP):
# get rid of all permissive exception concernign anIP
	table = iptc.Table(iptc.Table.FILTER)
	chain = iptc.Chain(table, "FORWARD")
	modified = True
	while modified:
		modified = False
		for rule in chain.rules:
			if anIP in rule.dst or anIP in rule.src :
		        	chain.delete_rule(rule)
				modified = True
				break

def retrieveUsage(anIP):
# retrieves absolute bytes flowed trough rules containing anIP
	table = iptc.Table(iptc.Table.FILTER)
	chain = iptc.Chain(table, "FORWARD")
	table.refresh()
	bytesUsed = 0
	for rule in chain.rules:
		if anIP in rule.dst or anIP in rule.src:
			(packets, bytes) = rule.get_counters()
			bytesUsed+=bytes
	return bytesUsed

def flushChain(aChain):
# flushes aChain
	table = iptc.Table(iptc.Table.FILTER)
	chain = iptc.Chain(table, aChain)
	chain.flush()

def setChainPolicy(aChain, aPolicy):
# set the policy of aChain 
	table = iptc.Table(iptc.Table.FILTER)
	chain = iptc.Chain(table, aChain)
	pol = iptc.Policy(aPolicy)
	chain.set_policy(pol, 0)
	
def allowSpecificWebsite(anIP):
	# IPTABLES -A FORWARD -d allowedSite -j ACCEPT
	# IPTABELS -A FORWARD -s allowedSite -j ACCEPT 
	'''
	# to do: need to allow DNS
	iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
	'''
	# iptables -A FORWARD -s $IP_CLIENT -j ACCEPT
	chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
	rule = iptc.Rule()
	rule.src = anIP 
	target = iptc.Target(rule, "ACCEPT")
	rule.target = target
	chain.append_rule(rule)
	# iptables -A FORWARD -d $IP_CLIENT -j ACCEPT
	rule2 = iptc.Rule()
	rule2.dst = anIP
	rule2.target = target
	chain.append_rule(rule2)





################################################################################


