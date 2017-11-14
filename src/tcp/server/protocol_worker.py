#!/usr/bin/python
'''
Sudoku Game Server-Side Protocol Worker (TCP)
Created on Nov 10, 2017

@author: basar
'''
# Imports----------------------------------------------------------------------
from multiprocessing import Queue
import threading
import logging
from socket import error as soc_error
from tcp.server import protocol
from tcp.common import tcp_receive, tcp_send
from socket import socket, AF_INET, SOCK_STREAM
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()
# Class Impl ------------------------------------------------------------------
class ProtocolWorker(threading.Thread):
    def __init__(self, client, session_list, callback):
	print client
        self.__callback = callback
	self.__session_list = session_list
	self.__client = client
        threading.Thread.__init__(self)
    
    def terminate(self):
	LOG.debug("Terminatig event bus...")
        self.__quit = True
        self.__q.put("DUMMY")

    def run(self):
	buf = ""
	self.__client["client_socket"].setblocking(0)
	while True:
	    m = None
	    try:
	        buf += self.__client["client_socket"].recv(512)
	    except (soc_error) as e:
		endofmsg = buf.find(";;")
		if endofmsg > 0:
		    m = buf[0:endofmsg]
		    buf = buf[endofmsg:len(buf)]	    
		    # Now here we assumen the message contains
		    LOG.debug('Received message [%d bytes]' % (len(m),))

		    # We are processing message we have
		    # TODO : Session Manager Needed
		    r = protocol.server_process(m)

		    # Try to send the response (r) to client
		    # Shutdown the TX pipe of the socket after sending
		    try:
			LOG.debug('Processed request for client %s:%d, '\
			  'sending response' % self.__client["addr"])
			# Send all data of the response (r)
			tcp_send(self.__client["client_socket"], r)
		    except soc_error as e:
			# In case we failed in the middle of transfer we should report error
			LOG.error('Interrupted sending the data to %s:%d, '\
			  'error: %s' % (self.__client["addr"]+(e,)))
			# ... and close socket
			#__disconnect_client(self.__client["client_socket"])
			self.__client["client_socket"] = None
			self.__callback(e, self.__client)
			# ... and we should proceed to destroy
			break

