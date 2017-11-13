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
    def __init__(self, args):
        self.__callback = args.close_callback
	self.__client = args.client
        threading.Thread.__init__(self)
    
    def terminate(self):
	LOG.debug("Terminatig event bus...")
        self.__quit = True
        self.__q.put("DUMMY")

    def run(self):
	while True:
	    m = None
	    try:
	        m = tcp_receive(self.__client.client_socket)
	    except (soc_error) as e:
	        # In case we failed in the middle of transfer we should report error
	        LOG.error('Interrupted receiving the data from %s:%d, '\
		  'error: %s' % (source+(e,)))
	        # ... and close socket
	        __disconnect_client(self.__client.client_socket)
		self.__client.client_socket = None
	        # ... and proceed to destroy client
		close_callback(e, self.__client)
	        break

	    # Now here we assumen the message contains
	    LOG.debug('Received message [%d bytes] '\
	      'from %s:%d' % ((len(m),)+self.__client.source))

	    # We are processing message we have
	    # TODO : Board gibi bi
	    r = protocol.server_process(m)

	    # Try to send the response (r) to client
	    # Shutdown the TX pipe of the socket after sending
	    try:
	        LOG.debug('Processed request for client %s:%d, '\
		  'sending response' % self.__client.source)
	        # Send all data of the response (r)
	        tcp_send(self.__client.client_socket, r)
	    except soc_error as e:
	        # In case we failed in the middle of transfer we should report error
	        LOG.error('Interrupted sending the data to %s:%d, '\
		  'error: %s' % (self.__client.source+(e,)))
	        # ... and close socket
	        __disconnect_client(self.__client.client_socket)
		client.client_socket = None
		close_callback(e, client)
	        # ... and we should proceed to destroy
	        break

