#!/usr/bin/python

import sys
import urllib2, json
import datetime
from websocket import create_connection


highestBlock = 0
result = "OK"
logFile = "/tmp/checkNode.log"
typeLog = 0


def writeLog(msg):
	global typeLog, logFile
	try:
		if (typeLog == 1): # stdout
			print("{}-{}\n".format(datetime.datetime.now(),msg))
		elif (typeLog == 2): # stderr
			sys.stderr.write("{}-{}\n".format(datetime.datetime.now(),msg))
		else: # textFile
			text_file = open(logFile, "a")
			text_file.write("{}-{}\n".format(datetime.datetime.now(),msg))
			text_file.close()
        
	except:
		{}
    
def doCheckEthSyncing(ipRpcNode, threshold):
    res = "OK"
    data = {"method":"eth_syncing","params":[],"id":1,"jsonrpc":"2.0"}
    writeLog("make POST to {} with params {}".format(ipRpcNode, data))
    try:
        req = urllib2.Request(ipRpcNode)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req, json.dumps(data))
        content = resp.read()
        response = json.loads(content)
        writeLog("Response:{}".format(response))
        if (response['result'] == False):
            return "OK"

        
        iniBlock = int(response['result']['currentBlock'],0)
        endBlock = int(response['result']['highestBlock'],0)
        writeLog("currentBlock:{} <=> highestBlock:{}".format(blockIni, blockFin))
        if (blockFin - blockIni > threshold):
            res = "ERR_SYNC"
            writeLog("Block difference greater than the threshold. Return ERR_SYNC")
            
    except Exception as e:
        writeLog("ERROR in doCheckEthSyncing:{}".format(e))
        res = "ERR_NET_NODE"
        
    return res
        
def getHighestBlock(urlEthStats):
    res = "OK"
    global highestBlock
    writeLog("open websocket {}".format(urlEthStats))
    try:
       
        ws = create_connection(urlEthStats)
        idx = 1
        while idx < 20:
            response =  ws.recv()
            res_json = json.loads(response)
            if (res_json['action']=='block'):
                if (int(res_json['data']['block']['number']) > highestBlock):
                    highestBlock = int(res_json['data']['block']['number'])
                idx += 1
        ws.close()
        writeLog("highestBlock block get in WS:{}".format(highestBlock))
            
    except Exception as e:
        writeLog("ERROR in getHighestBlock:{}".format(e))
        res = "ERR_NET_STAT"
        
    return res

def doCheckEthBlockNumber(ipRpc, highestBlock, threshold):
    res = "OK"
    data = {"method":"eth_blockNumber","params":[],"id":1,"jsonrpc":"2.0"}
    writeLog("make POST to {} with params {}".format(ipRpc, data))
    try:
        req = urllib2.Request(ipRpc)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req, json.dumps(data))
        content = resp.read()
        response = json.loads(content)
        writeLog("response:{}".format(response))        
        if (highestBlock - int(response['result'],0) > threshold):
            writeLog("Node not sync. [highestBlock:{}][bloqueNodo:{}][threshold{}]".format(highestBlock, int(response['result'],0), threshold))
            res = "ERR_SYNC"
            
    except Exception as e:
        writeLog("ERROR in doCheckEthBlockNumber:{}".format(e))
        res = "ERR_NET_NODE"
        
    return res    
    
if ((len(sys.argv)<4) or (len(sys.argv)>6)):
    print("Error. Incorrect params. Use:\n./checkNode.py ip_rpc_node url_ethstat threshold [check_eth_syncing=[0|1] [logSystem=[0|1|2]]]")
    sys.exit(0)

ipRpc = sys.argv[1]
urlEthStats = sys.argv[2]
threshold = int(sys.argv[3])
checkEthSyncing = True
typeLog = 0
if (len(sys.argv)==5):
    checkEthSyncing = (sys.argv[4]=="1")
if (len(sys.argv)==6):
	try:
		typeLog = int(sys.argv[5])
	except:
		typeLog =0

writeLog("Run with params [ip_rpc_nodo:{}][url_ethstat:{}][threshold:{}][check_eth_syncing:{}][logSystem:{}]".format(ipRpc,urlEthStats,threshold,checkEthSyncing, typeLog))
if (checkEthSyncing):
    result = doCheckEthSyncing(ipRpc, threshold)
if (result == "OK"):
    result = getHighestBlock(urlEthStats)
    if (result == "OK"):
        result = doCheckEthBlockNumber(ipRpc, highestBlock, threshold) 
   

print result