from txUtils import *




rKeyClient = 'L1Gxw9jdwGh2pow9H5hjhtMyiLK5o6mEdtGsrstMRtgp8gpvpzNy'
uKeyClient = privtopub(rKeyClient)

rKeyServer = 'KyEEnNgSwuBK3PwqAdsRMrPqhQ5xsm4WBgb7KFiAM7DYxaGsntq3'
uKeyServer = privtopub(rKeyServer)

script = mk_multisig_script(uKeyClient, uKeyServer, 2,2)

#if script != genscript: print 'pb'

payment = makePtx(uKeyClient, uKeyServer, balanceAddr(scriptaddr(script))-13000)

sigClient = multisign(payment, 0, script, rKeyClient)

sigServer= multisign(payment, 0, script, rKeyServer)

signed = apply_multisignatures(payment, 0, script, [sigClient, sigServer])

signed2= signAndCombine(payment, uKeyClient, sigClient, rKeyServer)

if signed != signed2: print 'signAndCombine is probably wrong'

print signed

pushtx(signed)
