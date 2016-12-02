'''
Created on Oct 10, 2016

@author: riaps
'''
from .port import Port
import threading
import zmq

class TimerThread(threading.Thread):
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.name = parent.instName
        self.context = parent.context
        self.period = parent.period * 0.001 # millisec
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        
    def run(self):
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('inproc://timer_' + self.name)
        while 1:
            self.active.wait(None)
            self.waiting.wait(self.period)
            if self.active.is_set():
                self.socket.send_string('tick')
            
    def activate(self):
        self.active.set()
    
    def deactivate(self):
        self.active.clear()
    
class TimPort(Port):
    '''
    classdocs
    '''

    def __init__(self, parentPart, portName, portSpec):
        '''
        Constructor
        '''
        super(TimPort,self).__init__(parentPart,portName)
        self.instName = self.parent.name + '.' + self.name
        self.period = portSpec["period"]

    def setup(self):
        self.thread = TimerThread(self)
        self.thread.start() 
    
    def setupSocket(self):
        assert self.instName == self.thread.name       
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('inproc://timer_' + self.instName)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')
        return ('tim',self.name)

    def activate(self):
        self.thread.activate()
        
    def deactivate(self):
        self.thread.deactivate()
        
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def recv_pyobj(self):
        res = self.socket.recv_string()
        return res
    
    def getInfo(self):
        return ("tim",self.name,"*tick*")
