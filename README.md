# alastria-monitoring
tools for monitoring Alastria network
# Utilidades

 - **checkNode.py**: Script que comprueba el estado de sincronismo de un nodo de Alastria. Utiliza el servicio RPC del nodo a comprobar y una instancia de EthNetstat del que obtiene el valor del último bloque de la Blockchain. Devuelve por consola el estado de sincronización del nodo:
	 - OK: Nodo sincronizado.
	 - ERR_SYNC: Nodo no sincronizado.
	 - ERR_NET_NODO: Error al conectar al RPC del nodo.
	 - ERR_NET_STAT: Error al acceder a la Url de EthStats.
Recibe por linea de comandos 4 parámetros:
	 - ipRpcNode: Ip del servicio RPC del nodo.
	 - urlEthStats: URL del servicio ethNetstat.
	 - umbral: Entero que permite un umbral entre el bloque del nodo y el del ethNetstat para decidir si el nodo está actualizado.
	 - checkLocal: Flag (0|1) que indica si antes de obtener el valor del bloque del ethNetstat, hace una llamada a la función *eth_syncing* que puede permitir saber el estado del nodo sin falta de acceder al servicio ethNetstat.

<code>
$ ./checkNode.py http://127.0.0.1:22000 ws://52.56.86.239:3000/primus/ 2 0
</code>