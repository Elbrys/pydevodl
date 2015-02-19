import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, Timeout
from requests import Response, codes

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

STATUS= enum('OK', 'CONN_ERROR',
             'DATA_NOT_FOUND', 'BAD_REQUEST',
             'UNAUTHORIZED_ACCESS', 'INTERNAL_ERROR',
             'NODE_CONNECTED', 'NODE_DISONNECTED',
             'NODE_NOT_FOUND', 'NODE_CONFIGURED',                   
             'HTTP_ERROR', 'N_A')

#===============================================================================
# 
#===============================================================================
class OperStatus(object):
#    ctrl_status=None
#    http_resp = Response()
#    pass
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

    def noerr(self):
        if(self.ctrl_status != STATUS.OK):
            return False        
#        if(self.http_resp != None):            
        pass

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
        elif( self.ctrl_status == STATUS.N_A):
            return "Unknown error"
        else:
            print ("Error: undefined status value %s" % self.ctrl_status)
            raise ValueError('!!!undefined status value')

'''
#-----------------------------------------------------------------------
#
#-----------------------------------------------------------------------
def http_get_request(url, data, headers):
#    status = OperStatus()
    resp = None
    
    adminName="admin"
    adminPassword="admin"
    timeout=5

    try:
        resp = requests.get(url,
                            auth=HTTPBasicAuth(adminName, adminPassword), 
                            data=data, headers=headers, timeout=timeout)
    except (ConnectionError, Timeout) as e:
        print "Error: " + repr(e)
    
    return (resp)



def check_node_config_status(nodeId):
    templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes111111111111"    
    status = OperStatus()
    
    ipAddr="172.22.18.186"
    portNum="8080"
    url = templateUrl.format(ipAddr, portNum)
    
    resp = http_get_request(url, data=None, headers=None)
    if(resp == None):
        status = OperStatus(STATUS.CONN_ERROR)
    elif (resp.status_code == 200):
        status = OperStatus(STATUS.NODE_CONFIGURED, resp)
    else:
        status = OperStatus(STATUS.DATA_NOT_FOUND, resp)
    
    return status

nodeName="TEST"
res = check_node_config_status(nodeName)
if (res.ctrl_status == STATUS.NODE_CONFIGURED):
#    print res.brief()
    print ("'%s' %s" % (nodeName, res.brief().lower()))
else:
    print ("Error!!! %s." % res.brief())
    print ("Failure reason: \n%s:" % res.detail())
'''
