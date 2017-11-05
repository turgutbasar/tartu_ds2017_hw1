#!/usr/bin/python
'''
Simplified File Transfer client (TCP)
Created on Oct 20, 2017

@author: basar
'''
# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Needed imports ------------------ -------------------------------------------
from tcp.mboard.sessions.client import protocol
from tcp.mboard.sessions.client.protocol import upload, download, list
from time import asctime
# Constants -------------------------------------------------------------------
___NAME = 'Simplified File Transfer Client'
___VER = '0.1.0.0'
___DESC = 'Simplified File Transfer Client (TCP version)'
___BUILT = '2017-10-20'
___VENDOR = 'Copyright (c) 2017 DSLab'
# Private methods -------------------------------------------------------------
def __info():
    return '%s version %s (%s) %s' % (___NAME, ___VER, ___BUILT, ___VENDOR)
# Not a real main method-------------------------------------------------------
def mboard_client_main(args):
    '''Runs the Simplified File Transfer client
    should be run by the main mehtod of CLI or GUI application
    @param args: ArgParse collected arguments
    '''
    # Starting client
    LOG.info('%s version %s started ...' % (___NAME, ___VER))
    LOG.info('Using %s version %s' % ( protocol.___NAME, protocol.___VER))

    # Processing arguments
    # 1.) If -f was provided
    f = ''
    if len(args.file) > 0:
        f = args.file # File Path

    # Server's socket address
    server = (args.host,int(args.port))
    try:
        if args.download:
            # No file existince check provided due to lack of time :)
            download(server, f)
        elif args.list:
            _, files = list(server)
            print("\nFiles--------\n")
            for item in files:
                print("%s" % item)
            print("-------------\n")
        else:
            upload(server, f)
    except KeyboardInterrupt:
        LOG.debug('Crtrl+C issued ...')
        LOG.info('Terminating ...')
        exit(2)

    print 'Terminating ...'
