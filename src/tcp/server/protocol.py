'''
Sudoku Game Server-Side Protocol (TCP)
Created on Nov 5, 2017

@author: basar
'''
# Setup Python logging --------------------------------------------------------
import logging

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()
# Imports----------------------------------------------------------------------
from exceptions import ValueError  # for handling number format exceptions
from tcp.common import __RSP_BADFORMAT, \
    __RSP_OK, __MSG_FIELD_SEP, __RSP_UNKNCONTROL, __REQ_REGISTRATION, __REQ_NEW_SESSION, __REQ_JOIN_EXISTING, \
    __REQ_BOARD_CHANGE, __REQ_CLIENT_LEFT
# TODO: add reqs
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


def server_process(chunk, session_manager, socket, addr):
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

    client_id = session_manager.get_client_id(addr)

    if chunk.startswith(__REQ_REGISTRATION + __MSG_FIELD_SEP):
        # Split payload
        args = chunk[2:].split(__MSG_FIELD_SEP)
        # adding username to the list
        session_manager.new_player(args[0], socket, addr)
        # getting session_list
        rsp = session_manager.get_session_list()
        # return session_list
        return rsp

    elif chunk.startwith(__REQ_NEW_SESSION + __MSG_FIELD_SEP):
        args = chunk[2:].split(__MSG_FIELD_SEP)
        session_id = session_manager.new_session(client_id)
        return session_id

    elif chunk.startwith(__REQ_JOIN_EXISTING + __MSG_FIELD_SEP):
        # TODO: Game starting broadcasting
        args = chunk[2:].split(__MSG_FIELD_SEP)
        # boshsa add to session manager
        join = session_manager.join_session(client_id, args[0])
        if (join == True):
            ready = session_manager.is_session_ready(arg[0])
            if (ready == True):
                # TODO: broadcasting game started
                i = 66666  # to fix indent
            else:
                return __RSP_OK
        else:
            # TODO: Correct error
            return "Error"

    elif chunk.startwith(__REQ_BOARD_CHANGE + __MSG_FIELD_SEP):
        # TODO: Game scores broadcasting, or anonse winner broadcasting
        args = chunk[2:].split(__MSG_FIELD_SEP)
        move = {'i': int(args[1]), 'j': int(args[2]), 'value': int(args[3])}
        game_status = session_manger.process_game_move(args[0], client_id, move)

        # broadcasting
        return __RSP_OK
    elif chunk.startwith(__REQ_CLIENT_LEFT + __MSG_FIELD_SEP):
        args = chunk[2:].split(__MSG_FIELD_SEP)
        status = session_manger.client_left_server(args[0], client_id)
        if status == False:
            # TODO: Finishing game
            # TODO: broadcasting
            i = 999999  #############
        return __RSP_OK
    else:
        LOG.debug('Unknown control message received: %s ' % chunk)
        return __RSP_UNKNCONTROL
