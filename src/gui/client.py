# Imports----------------------------------------------------------------------
# Main method -----------------------------------------------------------------
import sys

from socket import AF_INET, SOCK_STREAM, socket

def get_nickname(nickname):
    if (nickname != '') and (' ' not in nickname) and len(nickname) <= 8:
        return 1
    else:
        return 0

def get_address(ip,port):
    
    print 'Application started'
    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'
    print ip
    print port
    server_address = (ip,int(port))
    try:
        print "Connecting ..."
        s.connect(server_address)
        if s.sendall("connect") == None:
            sessions = s.recv(1024)
            print sessions
    except Exception as e:
        s.close()
        print e

def multiplayer_game_dialog():
    '''
    show session list
    print get_address(ip,port)'''
    # create session
    player_num = 3
    #create_sudoku_session(player_num)

#def create_sudoku_session(player_num):
    # register the session in server

#def join_sudoku_session():
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



