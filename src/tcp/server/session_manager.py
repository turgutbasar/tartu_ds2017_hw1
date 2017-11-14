#!/usr/bin/python
'''
Sudoku Game Server-Side Protocol Worker (TCP)
Created on Nov 10, 2017

@author: basar
'''
# Imports----------------------------------------------------------------------
from multiprocessing import Queue
import threading
import logging
from socket import error as soc_error
from tcp.server import protocol
from tcp.common import tcp_receive, tcp_send
from socket import socket, AF_INET, SOCK_STREAM
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()

client_numerator = 0
session_numerator = 0

# Class Impl ------------------------------------------------------------------
class SessionManager():
    def __init__(self):
        self.__sessionlist = []
	self.__clientlist = []
    def new_player(nickname, socket, addr):
        c = {"client_id": client_numerator, "client_socket": socket, "addr": addr}
	client_numerator += 1
	self.__clientlist.append(c)
	return client_numerator
    def new_session(client_id):
	client = self.__clienlist[client_id]
	game = {}
	session = {"session_id": session_numerator, "clients": [client], "game": game, "desired_player": 4, "score_board": dict.fromKeys([client_id])}
	session_numerator += 1
	self.__sessionlist.append(session)
	return session["session_id"]
    def join_session(client_id, session_id):
	session = self.__sessionlist[session_id]
	client = self.__clientlist[client_id]
	if len(session["clients"]) >= session["desired_player"]:
	    return False
	else:
	    session["clients"].append(client)
	    session["score_board"][client_id] = 0
	    return True
    def is_session_ready(session_id):
	session = self.__sessionlist[session_id]
	if len(session["clients"]) >= session["desired_player"]:
	    return True
	else:
	    return False
    def process_game_move(session_id, client_id, move):
	session = self.__sessionlist[session_id]
	game = session["game"]
	if game.check(move["i"], move["j"], move["value"]):
	    session["score_board"][client_id] += 1
	else:
	    session["score_board"][client_id] -= 1
	# TODO : Game needs a method like this
	return game.isEnded():   
    def client_left_session(session_id, client_id):
	session = self.__sessionlist[session_id]
	client = self.__clientlist[client_id]
	session["clients"].remove(client)
	# Checks if game ended
	if len(session["clients"]) < 2:
	    return False
	else
	    return True
    def client_left_server(client_id):
	# TODO : check every session to clean user and return ended games
    def get_client_id(addr):
	# TODO . match client address with client_id and return client id
     
