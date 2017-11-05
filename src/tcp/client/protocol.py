'''
Simplified File Transfer Protocol Client-Side (TCP)
Created on Oct 20, 2017

@author: basar
'''
# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Imports----------------------------------------------------------------------
from tcp.mboard.sessions.common import  __RSP_OK,  __RSP_ERRTRANSM, __RSP_CANT_CONNECT,\
     __CTR_MSGS, tcp_send, tcp_receive, MBoardProtocolError, __ERR_MSGS, __REQ_UPLOAD,__REQ_DOWNLOAD,__REQ_LIST, __MSG_FIELD_SEP,__REQ_UPLOAD_DATA, __RSP_BAD_FILE_NAME_OR_SIZE
from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_err
import os
# Constants -------------------------------------------------------------------
___NAME = 'Simplified File Transfer Protocol'
___VER = '0.1.0.0'
___DESC = 'State-less Simplified File Transfer Protocol Client-Side (TCP version)'
___BUILT = '2017-10-20'
___VENDOR = 'Copyright (c) 2017 DSLab'
# Static functions ------------------------------------------------------------
def __getfilesize(file):
    st = os.stat(file)
    return st.st_size
def __disconnect(sock):
    '''Disconnect from the server, close the TCP socket
    @param sock: TCP socket to close
    @param srv: tuple ( string:IP, int:port ), server's address
    '''
    # Usually we do not need separate method for just closing the socket
    # Here we do it because we can close socket in multiple place down in
    # __request method ... and we don not want to copy paste all the LOGs

    # Check if the socket is closed disconnected already ( in case there can
    # be no I/O descriptor
    try:
        sock.fileno()
    except soc_err:
        LOG.debug('Socket closed already ...')
        return

    # Closing RX/TX pipes
    LOG.debug('Closing client socket ...')
    # Close socket, remove I/O descriptor
    sock.close()
    LOG.info('Disconnected from server')

def __request(srv,r_type,args):
    '''Send request to server, receive response
    @param srv: tuple ( IP, port ), server socket address
    @param r_type: string, request type
    @param args: list, request parameters/data
    @returns tuple ( string:err_code, list:response arguments )
    '''

    # Declaring TCP socket
    sock = socket(AF_INET,SOCK_STREAM)
    LOG.debug('Client socket created, descriptor %d' % sock.fileno())

    # Try connect to server
    try:
        sock.connect(srv)
    except soc_err as e:
        # In case we failed to connect to server, we should report error code
        LOG.error('Can\'t connect to %s:%d, error: %s' % (srv+(e,)))
        return __RSP_CANT_CONNECT,[str(e)]
    LOG.info('Client connected to %s:%d' % srv)
    LOG.debug('Local TCP socket is bound on %s:%d' % sock.getsockname())

    # If we are connected
    # Envelope the request
    req = __MSG_FIELD_SEP.join([r_type]+map(str,args))
    LOG.debug('Will send [%s] request, total size [%d]'\
              '' % (__CTR_MSGS[r_type], len(req)))

    # Try to Send request using TCP
    n = 0   # Number of bytes sent
    try:
        n = tcp_send(sock, req)
    except soc_err as e:
        # In case we failed in the middle of transfer we should report error
        LOG.error('Interrupted sending the data to %s:%d, '\
                    'error: %s' % (sock+(e,)))
        # ... and close socket
        __disconnect(sock)
        return __RSP_ERRTRANSM,[str(e)]

    # We assume if we are here we succeeded with sending, and
    # we may start receiving
    rsp = None
    try:
        rsp = tcp_receive(sock)
    except (soc_err, MBoardProtocolError) as e:
        # In case we failed in the middle of transfer we should report error
        LOG.error('Interrupted receiving the data from %s:%d, '\
                  'error: %s' % (srv+(e,)))
        # ... and close socket
        __disconnect(sock)
        return __RSP_ERRTRANSM,[str(e)]

    # We assume if we are here we succeeded with receiving, and
    # we may close the socket and check the response
    LOG.debug('Received response [%d bytes] in total' % len(rsp))
    __disconnect(sock)

    # Check error code
    r_data = rsp.split(__MSG_FIELD_SEP)
    err,r_args = r_data[0],r_data[1:] if len(r_data) > 1 else []
    if err != __RSP_OK:
        if err in __ERR_MSGS.keys():
            LOG.error('Server response code [%s]: %s' % (err,__ERR_MSGS[err]))
        else:
            LOG.error('Malformed server response [%s]' % err)

    return err,r_args

def list(srv):
    '''Sends listing request to server, receive response
    @param srv: tuple ( IP, port ), server socket address
    @returns tuple ( boolean:result, list:files )
    '''   
    # Sending List Request
    err, _ = __request(srv, __REQ_LIST, [''])
    return err != __RSP_OK, _

def download(srv,file):
    '''Sends download request to server, receive response
    @param srv: tuple ( IP, port ), server socket address
    @param file: string: file name to download
    @returns boolean : result
    '''      
    # Sending Download request
    err, _ = __request(srv, __REQ_DOWNLOAD, [file])
    f = open(file, "w")
    f.write(_[0])
    f.close()
    return err != __RSP_OK


def upload(srv,file):
    '''Sends upload request to server, receive response
    @param srv: tuple ( IP, port ), server socket address
    @param file: string: file name to download
    @returns boolean : result
    '''      
    if check_file_name_and_size_avialable(srv, file):  
        with open(file) as f:
            content = f.read()
            # Sending Upload request
            err, _ = __request(srv, __REQ_UPLOAD_DATA, [content])
            return err != __RSP_OK
    return False

def check_file_name_and_size_avialable(srv,file):
    '''Ask if file name avialable
    @param src: tuple ( IP, port ), server socket address
    @param file: string, file_name
    @returns boolean : result
    '''
    # Sending File Name and Size Check request
    
    err, _ = __request(srv, __REQ_UPLOAD, [file, __getfilesize(file)])
    return err == __RSP_OK
