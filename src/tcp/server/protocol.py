'''
Sudoku Game Server-Side Protocol (TCP)
Created on Nov 5, 2017

@author: basar
'''
# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Imports----------------------------------------------------------------------
from exceptions import ValueError # for handling number format exceptions
from tcp.common import __RSP_BADFORMAT,\
     __REQ_SAMPLE, __RSP_OK, __MSG_FIELD_SEP, __RSP_UNKNCONTROL
from socket import error as soc_err
# Constants -------------------------------------------------------------------
___NAME = 'Sudoku Game Server-Side Protocol'
___VER = '0.1.0.0'
___DESC = 'Sudoku Game Server-Side Protocol (TCP version)'
___BUILT = '2017-11-5'
___VENDOR = 'Copyright (c) 2017 DSLab'
# Static functions ------------------------------------------------------------
def __disconnect_client(sock):
    '''Disconnect the client, close the corresponding TCP socket
    @param sock: TCP socket to close (client socket)
    '''

    # Check if the socket is closed disconnected already ( in case there can
    # be no I/O descriptor
    try:
        sock.fileno()
    except soc_err:
        LOG.debug('Socket closed already ...')
        return

    # Closing RX/TX pipes
    LOG.debug('Closing client socket')
    # Close socket, remove I/O descriptor
    sock.close()
    LOG.info('Disconnected client')

def server_process(chunk):
    '''Process the client's messages and generates needed events 
        @param event_bus: Event bus that has all event messages about server
        @param message: string, protocol data unit received from client
        @param source: tuple ( ip, port ), client's socket address
        @returns string, response to send to client
    '''
    LOG.debug('Received request [%d bytes] in total' % len(chunk))
    if len(chunk) < 2:
        LOG.debug('Not enough data received from %s ' % chunk)
        return __RSP_BADFORMAT
    LOG.debug('Request control code (%s)' % chunk[0])
    if chunk.startswith(__REQ_SAMPLE + __MSG_FIELD_SEP):
	# Split payload
        args = chunk[2:].split(__MSG_FIELD_SEP)
        return __RSP_OK
    else:
        LOG.debug('Unknown control message received: %s ' % chunk)
        return __RSP_UNKNCONTROL
