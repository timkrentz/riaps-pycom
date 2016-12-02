'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port
from riaps.run.exc import OperationError


class SrvPort(Port):
    '''
    classdocs
    '''


    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(SrvPort,self).__init__(parentComponent,portName)
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)

    def setup(self):
        pass
  
    def setupSocket(self):
        self.socket = self.context.socket(zmq.REP)
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost)
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + localHost)
            self.host = localHost
        return ('srv',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type), self.host,self.portNum)

    def update(self, host, port):
        raise OperationError("Unsupported update() on SrvPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def recv_pyobj(self):
        return self.socket.recv_pyobj()
    
    def send_pyobj(self,msg):
        self.socket.send_pyobj(msg)
        
    def getInfo(self):
        return ("srv",self.Name,self.Type,self.host,self.portNum)