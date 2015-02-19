#import requests
#from requests.auth import HTTPBasicAuth
#from requests.exceptions import ConnectionError, Timeout
#from requests import Response, codes

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

STATUS = enum('OK', 'CONN_ERROR',
              'DATA_NOT_FOUND', 'BAD_REQUEST',
              'UNAUTHORIZED_ACCESS', 'INTERNAL_ERROR',
              'NODE_CONNECTED', 'NODE_DISONNECTED',
              'NODE_NOT_FOUND', 'NODE_CONFIGURED',                   
              'HTTP_ERROR', 'UNKNOWN')

#===============================================================================
# 
#===============================================================================
class OperStatus(object):

    def __init__(self, status=None, http_resp=None):
        self.ctrl_status = status
        self.http_resp = http_resp

    def set_status(self, ctrl_status, http_resp=None):
        self.ctrl_status=ctrl_status
        self.http_resp=http_resp
        
    def to_string(self):
        return self.ctrl_status_string()

    def brief(self):
        return self.ctrl_status_string()
    
    def detail(self):
        if(self.http_resp != None and self.http_resp.content != None):
            return self.http_resp.content
        else:
            return ""

    def opcode(self):
        return self.ctrl_status
    
    def eq(self, code):
        if(self.ctrl_status == code):
            return True
        else:
            return False
    '''
    def noerr(self):
        if(self.ctrl_status != STATUS.OK):
            return False        
#        if(self.http_resp != None):            
        pass
    '''

    def ctrl_status_string(self):
        if (self.ctrl_status == STATUS.OK):
            return "Success"
        elif( self.ctrl_status == STATUS.CONN_ERROR):
            return "Server connection error"
        elif( self.ctrl_status == STATUS.DATA_NOT_FOUND):
            return "Requested data not found"
        elif( self.ctrl_status == STATUS.BAD_REQUEST):
            return "Bad or invalid data in request"
        elif( self.ctrl_status == STATUS.UNAUTHORIZED_ACCESS):
            return "Server unauthorized access"
        elif( self.ctrl_status == STATUS.INTERNAL_ERROR):
            return "Internal Server Error"        
        elif( self.ctrl_status == STATUS.NODE_CONNECTED):
            return "Node is connected"
        elif( self.ctrl_status == STATUS.NODE_DISONNECTED):
            return "Node is disconnected"
        elif( self.ctrl_status == STATUS.NODE_NOT_FOUND):
            return "Node not found"
        elif( self.ctrl_status == STATUS.NODE_CONFIGURED):
            return "Node is configured"
        elif( self.ctrl_status == STATUS.HTTP_ERROR):
            return "HTTP error"
        elif( self.ctrl_status == STATUS.UNKNOWN):
            return "Unknown error"
        else:
            print ("Error: undefined status value %s" % self.ctrl_status)
            raise ValueError('!!!undefined status value')
