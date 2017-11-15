# Imports----------------------------------------------------------------------
# Main method -----------------------------------------------------------------
import sys
import threading
from socket import error as soc_error
import json

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()

TCP_RECEIVE_BUFFER_SIZE = 1024 * 1024
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
__ERR_MSGS = { __RSP_OK:'No Error',
               __RSP_SESSION_LIST:'Incoming session list',
               __RSP_BADFORMAT:'Malformed message',
               __RSP_UNKNCONTROL:'Unknown control code',
               __RSP_ERRTRANSM:'Transmission Error',
               __RSP_BOARD:'Game Board',
               __RSP_CANT_CONNECT:'Can\'t connect to server'
              }
from socket import AF_INET, SOCK_STREAM, socket


def get_nickname(nickname):
    if (nickname != '') and (' ' not in nickname) and len(nickname) <= 8:
        return 1
    else:
        return 0



def get_address(ip, port, nick_name, notify_callback):
    print 'Application started'
    global s
    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'
    print ip
    print port
    server_address = (ip, int(port))
    try:
        print "Connecting ..."
        s.connect(server_address)
        t = threading.Thread(target=tcp_receive_thread, args=(notify_callback, ))
        t.start()
        message = __MSG_FIELD_SEP.join([__REQ_REGISTRATION] + map(str, [nick_name])) + ";;"
        print message
        s.setblocking(0)
        s.sendall(message)
    except Exception as e:
        s.close()
        print e


def tcp_receive_thread(notify_callback):
    callback = notify_callback
    buf = ""
    s.settimeout(1)
    while True:
        try:
            buf += s.recv(1024)
        except soc_error as e:
            endofmsg = buf.find(";;")
            if endofmsg > 0:
                m = buf[0:endofmsg]
                buf = buf[endofmsg:len(buf)]
                # Now here we assumen the message contains
                LOG.debug(m)
                if len(m) < 2:
                    LOG.debug('Not enough data received from %s ' % m)
                    continue
                LOG.debug('Request control code (%s)' % m[0])

                if m.startswith(__RSP_SESSION_LIST + __MSG_FIELD_SEP):
                    # Split payload
                    args = m[2:].split(__MSG_FIELD_SEP)
                    key = '"session":'
                    data = "{"+key + args+"}"
                    print(data)
                    d = json.loads(data)
                    print (d["session"])
                    data = json.load(args)
                    callback(0, data)
                elif m.startswith(__RSP_BOARD + __MSG_FIELD_SEP):
                    # Split payload
                    args = m[2:].split(__MSG_FIELD_SEP)
                    key = '"session":'
                    data = "{"+key + args+"}"
                    print(data)
                    d = json.loads(data)
                    print (d["session"])
                    data = json.load(args)
                    callback(1, data)
                else:
                    LOG.debug('Unknown control message received: %s ' % m)


def send_session_id(id):
    try:
        message = __MSG_FIELD_SEP.join([__REQ_REGISTRATION] + map(str, [id])) + ";;"
        print message
        s.sendall(message)
    except Exception as e:
        s.close()
        print e


def create_game_session(players_num):
    try:
        print players_num
        if s.sendall(players_num) == None:
            session_id = s.recv(1024)
            return session_id
    except Exception as e:
        s.close()
        print e
    '''
    show session list
    print get_address(ip,port)'''
    # create session
    player_num = 3
    # create_sudoku_session(player_num)


# def create_sudoku_session(player_num):
# register the session in server

# def join_sudoku_session():
# open the game player dialog

'''if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    #a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
   # path.append(a_path)
    # Parsing arguments

    get nickname from ui
    name = sys.argv[1]
    print get_nickname(name)
    ip = sys.argv[1]
    port = sys.argv[2]
    print get_address(ip,int(port))'''
