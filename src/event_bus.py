'''
Pub-Sub Model Impl
Created on Nov 5 , 2017
@author: basar
'''
# Imports----------------------------------------------------------------------
from multiprocessing import Queue
import threading
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()
# Class Impl ------------------------------------------------------------------
class EventBus(threading.Thread):
    def __init__(self):
        self.__q = Queue()
	self.__quit = False
        threading.Thread.__init__(self)
    
    def subscribe(self, sub):
	self.__subscribers.append(sub)
    
    def add(self, evt):
	self.__q.append(evt)

    def terminate(self):
	LOG.debug("Terminatig event bus...")
        self.__quit = True
        self.__q.put("DUMMY")

    def run(self):
	while True:
            itm = self.__q.get()
            if self.__quit:
		break;
            for sub in self.__subscribers:
	        sub.handle(itm)
            LOG.debug("Next Item")
