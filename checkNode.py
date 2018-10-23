#!/usr/bin/python
import sys
import urllib2, json
import datetime
from websocket import create_connection

mayorBloque = 0
result = "OK"
log_file="/tmp/checkNode.log"

def escribeLog(msg):
    try:
        text_file = open(log_file, "a")
        text_file.write("{}-{}\n".format(datetime.datetime.now(),msg))
        text_file.close()
        
    except:
        {}
    
    


    
    
def doCheckEthSyncing(ip_rpc_nodo, umbral):
    res = "OK"
    data = {"method":"eth_syncing","params":[],"id":1,"jsonrpc":"2.0"}
    escribeLog("haciendo peticion POST a {} con parametros {}".format(ip_rpc_nodo, data))
    try:
        req = urllib2.Request(ip_rpc_nodo)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        contenido = response.read()
        respuesta = json.loads(contenido)
        escribeLog("Respuesta obtenida:{}".format(respuesta))
        if (respuesta['result'] == False):
            return "OK"

        
        blockIni = int(respuesta['result']['currentBlock'],0)
        blockFin = int(respuesta['result']['highestBlock'],0)
        escribeLog("currentBlock:{} <=> highestBlock:{}".format(blockIni, blockFin))
        if (blockFin - blockIni > umbral):
            res = "ERR_SYNC"
            escribeLog("Diferencia de bloques mayor que el umbral. Devuelvo ERR_SYNC")
            
        
        
    except Exception as e:
        escribeLog("ERROR en doCheckEthSyncing:{}".format(e))
        res = "ERR_NET_NODO"
        
    return res
        
def getHighestBlock(urlEthStats):
    res = "OK"
    global mayorBloque
    escribeLog("Abriendo websocket en {}".format(urlEthStats))
    try:
       
        ws = create_connection(urlEthStats)
        idx = 1
        while idx < 20:
            response =  ws.recv()
            res_json = json.loads(response)
            if (res_json['action']=='block'):
                if (int(res_json['data']['block']['number']) > mayorBloque):
                    mayorBloque = int(res_json['data']['block']['number'])
                idx += 1
        ws.close()
        escribeLog("Mayor bloque obtenido del WS:{}".format(mayorBloque))
            
    except Exception as e:
        escribeLog("ERROR en getHighestBlock:{}".format(e))
        res = "ERR_NET_STAT"
        
    return res

def doCheckEthBlockNumber(ipRpc, mayorBloque, umbral):
    res = "OK"
    data = {"method":"eth_blockNumber","params":[],"id":1,"jsonrpc":"2.0"}
    escribeLog("haciendo peticion POST a {} con parametros {}".format(ipRpc, data))
    try:
        req = urllib2.Request(ipRpc)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        contenido = response.read()
        respuesta = json.loads(contenido)
        escribeLog("Respuesta obtenida:{}".format(respuesta))        
        if (mayorBloque - int(respuesta['result'],0) > umbral):
            escribeLog("El nodo no esta actualizado. [MayorBloque:{}][bloqueNodo:{}][umbral{}]".format(mayorBloque, int(respuesta['result'],0), umbral))
            res = "ERR_SYNC"
            
    except Exception as e:
        escribeLog("ERROR en doCheckEthBlockNumber:{}".format(e))
        res = "ERR_NET_NODO"
        
    return res    
    
if ((len(sys.argv)<4) or (len(sys.argv)>5)):
    print("Error. Parametros incorrectos. Uso:\n./checkNode.py ip_rpc_nodo url_ethstat umbral [check_eth_syncing]")
    sys.exit(0)

ipRpc = sys.argv[1]
urlEthStats = sys.argv[2]
umbral = int(sys.argv[3])
checkEthSyncing = True
if (len(sys.argv)==5):
    checkEthSyncing = (sys.argv[4]=="1")

escribeLog("Ejecucion con parametro [ip_rpc_nodo:{}][url_ethstat:{}][umbral:{}][check_eth_syncing:{}]".format(ipRpc,urlEthStats,umbral,checkEthSyncing))
if (checkEthSyncing):
    result = doCheckEthSyncing(ipRpc, umbral)
if (result == "OK"):
    result = getHighestBlock(urlEthStats)
    if (result == "OK"):
        result = doCheckEthBlockNumber(ipRpc, mayorBloque, umbral) 
   

print result