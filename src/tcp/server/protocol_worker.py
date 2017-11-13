'''
Sudoku Game Server-Side Protocol Worker (TCP)
Created on Nov 10, 2017

@author: basar
'''
# Imports----------------------------------------------------------------------
from multiprocessing import Queue
import threading
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()
# Class Impl ------------------------------------------------------------------
class ProtocolWorker(threading.Thread):
    def __init__(self, callback):
        self.__callback = callback
        threading.Thread.__init__(self)
    
    def terminate(self):
	LOG.debug("Terminatig event bus...")
        self.__quit = True
        self.__q.put("DUMMY")

    def run(self):
	while True:
	    m = None
	    try:
	        m = tcp_receive(client.client_socket)
	    except (soc_error) as e:
	        # In case we failed in the middle of transfer we should report error
	        LOG.error('Interrupted receiving the data from %s:%d, '\
		  'error: %s' % (source+(e,)))
	        # ... and close socket
	        __disconnect_client(client.client_socket)
		client.client_socket = None
	        # ... and proceed to destroy client
		close_callback(e, client)
	        break

	    # Now here we assumen the message contains
	    LOG.debug('Received message [%d bytes] '\
	      'from %s:%d' % ((len(m),)+client.source))

	    # We are processing message we have
	    # TODO : Board gibi bir veri yapısı gerekiyorsa
	    r = protocol.server_process(m)

	    # Try to send the response (r) to client
	    # Shutdown the TX pipe of the socket after sending
	    try:
	        LOG.debug('Processed request for client %s:%d, '\
		  'sending response' % client.source)
	        # Send all data of the response (r)
	        tcp_send(client.client_socket, r)
	    except soc_error as e:
	        # In case we failed in the middle of transfer we should report error
	        LOG.error('Interrupted sending the data to %s:%d, '\
		  'error: %s' % (client.source+(e,)))
	        # ... and close socket
	        __disconnect_client(client.client_socket)
		client.client_socket = None
		close_callback(e, client)
	        # ... and we should proceed to destroy
	        break
