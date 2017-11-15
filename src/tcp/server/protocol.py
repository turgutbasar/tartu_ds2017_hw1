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
from exceptions import ValueError # for handling number format exceptions
from tcp.common import __RSP_BADFORMAT,\
     __RSP_OK, __MSG_FIELD_SEP, __RSP_UNKNCONTROL, __REQ_REGISTRATION, __REQ_NEW_SESSION, __REQ_JOIN_EXISTING, __REQ_BOARD_CHANGE, __REQ_CLIENT_LEFT, __RSP_SESSION_LIST, __RSP_BOARD, __RSP_SESSION_IS_FULL, __RSP_ENDGAME, __RSP_BOARDUPDATE
    #TODO: add reqs
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
    

    if chunk.startswith(__REQ_REGISTRATION + __MSG_FIELD_SEP):
        # Split payload
        args = chunk[2:].split(__MSG_FIELD_SEP)
        # adding username to the list
        session_manager.new_player(args[0], socket, addr)
        # getting session_list
        session_list = session_manager.get_session()
        #formatting
        rsp = __MSG_FIELD_SEP.join([__RSP_SESSION_LIST] + map(str, [session_list]))
        # return session_list
        return rsp

    elif chunk.startwith(__REQ_NEW_SESSION + __MSG_FIELD_SEP):
        client_id = session_manager.get_client_id(addr)
        args = chunk[2:].split(__MSG_FIELD_SEP)
        session_id = session_manager.new_session(client_id)
        return session_id
    #join session request
    elif chunk.startwith(__REQ_JOIN_EXISTING + __MSG_FIELD_SEP):
        # TODO: Game starting broadcasting
        client_id = session_manager.get_client_id(addr)
        args = chunk[2:].split(__MSG_FIELD_SEP)
        join = session_manager.join_session(client_id, args[0])
        #Join session if there is free place
        if(join == True):
            session_ready = session_manager.is_session_ready(args[0])
            #If game is ready to start
            if(session_ready != False):
                clients = session_ready[0]
                string = session_ready[1]
                #Broadcasting game board
                for c in clients:
                    message = __MSG_FIELD_SEP.join([__RSP_BOARD] + map(str, [string]))
                    c.sendall(message)
            return __RSP_OK
        else:
            return __RSP_SESSION_IS_FULL
    
    #add digit to game board request
    elif chunk.startwith(__REQ_BOARD_CHANGE + __MSG_FIELD_SEP):
        # TODO: Game scores broadcasting, or anonse winner broadcasting
        client_id = session_manager.get_client_id(addr)
        args = chunk[2:].split(__MSG_FIELD_SEP)

        move = {'i': int(args[1]), 'j':int(args[2]), 'value':int(args[3])}
        status = session_manager.process_game_move(args[0], client_id, move)
        clients = status[0]
        string = status[1]
        if(status[0] == True):            
            for c in clients:
                #broadcasting
                message = __MSG_FIELD_SEP.join([__RSP_ENDGAME] + map(str, [string]))
                c.sendall(message)
        else:
            for c in clients:
                message = __MSG_FIELD_SEP.join([__RSP_BOARDUPDATE] + map(str, [string]))
                c.sendall(message)

        return __RSP_OK
    
    #client left game request
    elif chunk.startwith(__REQ_CLIENT_LEFT + __MSG_FIELD_SEP):
        client_id = session_manager.get_client_id(addr)
        args = chunk[2:].split(__MSG_FIELD_SEP)
        status = session_manager.client_left_session(args[0],client_id)
        clients = status[0]
        string = status[1]
        #broadcasting
        if(status[0] == True):            
            for c in clients:
                message = __MSG_FIELD_SEP.join([__RSP_ENDGAME] + map(str, [string]))
                c.sendall(message)
        else:
            for c in clients:
                message = __MSG_FIELD_SEP.join([__RSP_BOARDUPDATE] + map(str, [string]))
                c.sendall(message)

        return __RSP_OK
    else:
        LOG.debug('Unknown control message received: %s ' % chunk)
        return __RSP_UNKNCONTROL
