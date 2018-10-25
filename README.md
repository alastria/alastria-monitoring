# alastria-monitoring
Tools for monitoring Alastria network

## Utilities

### **checkNode.py**

This script performs a syncing check on a given node in Alastria network. Compares the last block value coming from an Eth-Netats instance and the value returned by the RPC service of said node. Returns the syncing status of the node:
- **OK**: Node is synchronized
- **ERR_SYNC**: Node is not synchronized
- **ERR_NET_NODE**: Error connecting to the RPC services
- **ERR_NET_STAT**: Error reaching Eth-Netats URL

Takes 5 arguments:
- **ipRpcNode**: Node's RPC service IP address
- **urlEthNetstats**: Eth-Netstats instance URL
- **threshold**: Maximum allowed difference between the two values so the node is considered synchronized
- **checkLocal**: [Optional] Flag (0|1). If set, checks first RPC *eth_syncing* locally before accesing the Eth-Netats service
- **logSystem**: [Optional] Selector (0|1|2)
	- 0, file
	- 1, standard output
	- 2, error output

Usage example:

<code>
$ ./checkNode.py http://127.0.0.1:22000 ws://52.56.86.239:3000/primus/ 2 0 1
</code>

Requires python _websocket-client_ library

<code>
$     pip install websocket-client
</code>
