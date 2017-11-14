'''
Sudoku Game Server - Main
Created on Nov 5 , 2017
@author: basar
'''
# Imports----------------------------------------------------------------------
from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from os.path import abspath, sep
from tcp.server.main import __info, ___VER, server_main
from tcp.common import DEFAULT_SERVER_INET_ADDR, DEFAULT_SERVER_PORT
import time
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()
# Main method -----------------------------------------------------------------
if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    # Parsing arguments
    parser = ArgumentParser(description=__info(),
                            version = ___VER)
    parser.add_argument('-l','--listenaddr', \
                        help='Bind server socket to INET address, '\
                        'defaults to %s' % DEFAULT_SERVER_INET_ADDR, \
                        default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p','--listenport', \
                        help='Bind server socket to UDP port, '\
                        'defaults to %d' % DEFAULT_SERVER_PORT, \
                        default=DEFAULT_SERVER_PORT)
    args = parser.parse_args()
    try:
	server_main(args)
    except KeyboardInterrupt:
	LOG.info('Terminating server ...')
