#!/usr/bin/python

from tcp.server.protocol import __disconnect_client
from tcp.server.protocol_worker import ProtocolWorker
from tcp.server.session_manager import SessionManager
'''
Sudoku Game Server (TCP)
Created on Nov 5, 2017

@author: basar
'''
# Setup Python logging ------------------ -------------------------------------
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()
# Imports ---------------------------------------------------------------------
from tcp.server import protocol
from tcp.common import tcp_receive, tcp_send
from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_error
from sys import exit
# Constants -------------------------------------------------------------------
___NAME = 'Sudoku Game Server'
___VER = '0.1.0.0'
___DESC = 'Sudoku Game Server (TCP version)'
___BUILT = '2017-11-5'
___VENDOR = 'Copyright (c) 2017 DSLab'
# -----------------------------------------------------------------------------
# How many clients may there be awaiting to get connection if the server is
# currently busy processing the other request
__DEFAULT_SERVER_TCP_CLIENTS_QUEUE = 10
# Private methods -------------------------------------------------------------
def __info():
    return '%s version %s (%s) %s' % (___NAME, ___VER, ___BUILT, ___VENDOR)
# Not a real main method-------------------------------------------------------
def server_main(args):
    '''Runs the sudoku game server
    should be run by the main mehtod of CLI or GUI application
    @param bus: Event Bus
    @param args: ArgParse collected arguments
    '''
    # Starting server
    LOG.info('%s version %s started ...' % (___NAME, ___VER))
    LOG.info('Using %s version %s' % ( protocol.___NAME, protocol.___VER))
        
    # Declaring TCP socket
    __server_socket = socket(AF_INET,SOCK_STREAM)
    LOG.debug('Server socket created, descriptor %d' % __server_socket.fileno())
    # Bind TCP Socket
    try:
        __server_socket.bind((args.listenaddr,int(args.listenport)))
    except soc_error as e:
        LOG.error('Can\'t start sudoku game server, error : %s' % str(e))
        exit(1)

    LOG.debug('Server socket bound on %s:%d' % __server_socket.getsockname())

    # Put TCP socket into listening state
    __server_socket.listen(__DEFAULT_SERVER_TCP_CLIENTS_QUEUE)
    LOG.info('Accepting requests on TCP %s:%d' % __server_socket.getsockname())

    # Client List
    client_list = []

    session_list = []

    worker_list = []

    client_numerator = 0
	

    # Serve forever
    while 1:
        try:
            LOG.debug('Awaiting new client connections ...')
            # Accept client's connection store the client socket into
            # client_socket and client address into source
            client_socket,source = __server_socket.accept()
            LOG.debug('New client connected from %s:%d' % source)
		
            client_numerator += 1
            client = {"client_id": client_numerator, "client_socket": client_socket, "addr": source}
            client_list.append(client)

            # Handles incoming connection requests, creates new worker, asigns client to worker
            # Worker need to handle protocol, messaging.
            def close_callback(e, c):
                LOG.debug(e);
                return;

            worker = ProtocolWorker(client, session_list, close_callback)

            worker_list.append(worker)

            worker.run()

        except KeyboardInterrupt as e:
            LOG.info('Terminating socket communication ...')
            break

    # If we were interrupted, make sure client socket is also closed
    for client in client_list:
        if client["client_socket"] != None:
            __disconnect_client(client["client_socket"])

    # Close server socket
    __server_socket.close()
    LOG.debug('Server socket closed')
    raise KeyboardInterrupt("")
