'''
Common variables, methods and structures of tcp modules
Created on Nov 5, 2016

@author: basar
'''
# Imports----------------------------------------------------------------------
from socket import SHUT_WR, SHUT_RD
from exceptions import Exception
# TCP related constants -------------------------------------------------------
#
DEFAULT_SERVER_PORT = 7777
DEFAULT_SERVER_INET_ADDR = '127.0.0.1'
#
# When receiving big messages in multiple blocks from the TCP stream
# the receive buffer size should be select according to amount of RAM available
# (more RAM = bigger blocks = less receive cycles = faster delivery)
TCP_RECEIVE_BUFFER_SIZE = 1024*1024
#
# protocol constants ----------------------------------------------------------
# Field separator for sending multiple values ---------------------------------
__MSG_FIELD_SEP = ':'
# Requests --------------------------------------------------------------------
__REQ_REGISTRATION = '1'
__REQ_NEW_SESSION = '2'
__REQ_JOIN_EXISTING = '3'
__REQ_BOARD_CHANGE = '4'
__REQ_CLIENT_LEFT = '5'

__CTR_MSGS = { __REQ_REGISTRATION:'Registration', __REQ_NEW_SESSION:'New session', __REQ_JOIN_EXISTING:'Join existing', __REQ_BOARD_CHANGE:'Game board change'
             }

# Responses--------------------------------------------------------------------
__RSP_OK = '0'
__RSP_BADFORMAT = '1'
__RSP_UNKNCONTROL = '3'
__RSP_ERRTRANSM = '4'
__RSP_CANT_CONNECT = '5'
__RSP_SESSION_LIST = '6'
__RSP_BOARD = '7'
__RSP_SESSION_IS_FULL = '8'
__RSP_ENDGAME = '9'
__RSP_BOARDUPDATE = '10'
__ERR_MSGS = { __RSP_OK:'No Error',
               __RSP_BADFORMAT:'Malformed message',
               __RSP_UNKNCONTROL:'Unknown control code',
               __RSP_ERRTRANSM:'Transmission Error',
               __RSP_CANT_CONNECT:'Can\'t connect to server'
               __RSP_SESSION_LIST:'Session list'
               __RSP_BOARD:'Game board'
               __RSP_SESSION_IS_FULL:'Session is full'
              }
# Common methods --------------------------------------------------------------
def tcp_send(sock,data):
    '''Send data using TCP socket. When the data is sent, close the TX pipe
    @param sock: TCP socket, used to send/receive
    @param data: The data to be sent
    @returns integer,  n bytes sent and error if any
    @throws socket.errror in case of transmission error
    '''
    sock.sendall(data)
    #sock.shutdown(SHUT_WR)
    return len(data)

def tcp_receive(sock,buffer_size=TCP_RECEIVE_BUFFER_SIZE):
    '''Receives data using TCP socket. When the data block is received, appends to
    m variable. Finally, it returns m value.
    @param sock: TCP socket, used to send/receive
    @param data: The data to be sent
    @returns integer,  n bytes sent and error if any
    @throws socket.errror in case of transmission error
    '''
    m = ''
    # Receive loop
    while 1:
        # Receive one block of data according to receive buffer size        
	block = sock.recv(TCP_RECEIVE_BUFFER_SIZE)
        # If the remote end-point did issue shutdown on the socket
        # using  SHUT_WR flag, the local end point will receive and
        # empty string in all attempts of recv method. Therefore we
        # say we stop receiving once the first empty block was received
        if len(block) <= 0:
            break
        m += block
    return m
