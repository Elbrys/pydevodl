'''
Created on Feb 3, 2015

@author: sergei
'''

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
#import pprint
import xmltodict
import json

#================================
# KEEP
#================================
def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

CTRL_STATUS = enum('OK', 'CONN_ERROR', 'DATA_NOT_FOUND', 'BAD_REQUEST', 'UNAUTHORIZED_ACCESS', 'N_A')
NODE_STATUS = enum('CONNECTED', 'DISONNECTED', 'NOT_FOUND', 'CONFIGURED', 'N_A')

#================================
# KEEP
#================================
class Status(object):
    def __init__(self, status):
        if status not in (CTRL_STATUS.OK,
                          CTRL_STATUS.CONN_ERROR,
                          CTRL_STATUS.DATA_NOT_FOUND,
                          CTRL_STATUS.BAD_REQUEST,
                          CTRL_STATUS.UNAUTHORIZED_ACCESS,
                          CTRL_STATUS.N_A,
                          NODE_STATUS.CONNECTED,
                          NODE_STATUS.DISONNECTED,
                          NODE_STATUS.NOT_FOUND,
                          NODE_STATUS.CONFIGURED,
                          NODE_STATUS.N_A
                          ):
            raise ValueError('undefined status value')
        self.status = status
    
    def string(self):
        if (self.status == CTRL_STATUS.OK):
            return "success"
        if( self.status == CTRL_STATUS.CONN_ERROR):
            return "server connection error"
        if( self.status == CTRL_STATUS.DATA_NOT_FOUND):
            return "requested data is not found"
        if( self.status == CTRL_STATUS.BAD_REQUEST):
            return "bad or invalid data in request"
        if( self.status == CTRL_STATUS.UNAUTHORIZED_ACCESS):
            return "server unauthorized access"
        if( self.status == CTRL_STATUS.N_A):
            return "unknown error"        
        if( self.status == NODE_STATUS.CONNECTED):
            return "node is connected"
        if( self.status == NODE_STATUS.DISONNECTED):
            return "node is disconnected"
        if( self.status == NODE_STATUS.NOT_FOUND):
            return "unknown error"
        if( self.status == NODE_STATUS.CONFIGURED):
            return "node is configured"
        if( self.status == NODE_STATUS.N_A):
            return "unknown error"

#================================
# KEEP
#================================
class Controller(object):
    def __init__(self, ipAddr, portNum, adminName, adminPassword):
        self.ipAddr = ipAddr
        self.portNum = portNum
        self.adminName = adminName
        self.adminPassword = adminPassword

    def ctrl_get_request(self, url, uname, passwd):
        resp = None
        status = None            

        try:
            resp = requests.get(url, auth=HTTPBasicAuth(uname, passwd))
            status = CTRL_STATUS.OK
        except ConnectionError:
            status = CTRL_STATUS.CONN_ERROR
        
        return (status, resp)
    
    def ctrl_post_request(self, url, data, headers, uname, passwd):
        resp = None
        status = None            

        try:
            resp = requests.post(url, auth=HTTPBasicAuth(self.adminName, self.adminPassword),
                                 data=data, headers=headers)
            status = CTRL_STATUS.OK
        except ConnectionError:
            status = CTRL_STATUS.CONN_ERROR
        
        return (status, resp)

    def check_node_config_status(self, nodeId):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
        
        result = self.ctrl_get_request(url, self.adminName, self.adminPassword)
        status = result[0]
        if (status == CTRL_STATUS.CONN_ERROR):
            return status
        
        response = result[1]
        if (response.status_code == 401):
            return CTRL_STATUS.UNAUTHORIZED_ACCESS    
        
        if (response.status_code == 400):
            return CTRL_STATUS.BAD_REQUEST
    
        if (response.status_code == 200):
            elemlist = json.loads(response.content).get('nodes').get('node')
            status = NODE_STATUS.NOT_FOUND
            for elem in elemlist:
                if(elem['id'] == nodeId):
                    status = NODE_STATUS.CONFIGURED
        
        return status
    
    def check_node_conn_status(self, nodeId):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
           
        result = self.ctrl_get_request(url, self.adminName, self.adminPassword)
        status = result[0]
        if (status == CTRL_STATUS.CONN_ERROR):
            return status
        
        response = result[1]
        if (response.status_code == 401):
            return CTRL_STATUS.UNAUTHORIZED_ACCESS    
        
        if (response.status_code == 400):
            return CTRL_STATUS.BAD_REQUEST
        
        if (response.status_code == 200):
            elemlist = json.loads(response.content).get('nodes').get('node')
            status = NODE_STATUS.NOT_FOUND
            for elem in elemlist:
                if(elem['id'] == nodeId):
                    status = NODE_STATUS.DISONNECTED
                    if (('netconf-node-inventory:connected' in elem) and
                        (elem['netconf-node-inventory:connected'] == True)):
                        status = NODE_STATUS.CONNECTED                        
                    break
        
        return status

    def get_all_nodes_in_config(self):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)        
        nlist = [] 
        
        result = self.ctrl_get_request(url, self.adminName, self.adminPassword)
        status = result[0]
        if (status == CTRL_STATUS.CONN_ERROR):
            return status
       
        response = result[1]
        if (response.status_code == 401):
            return CTRL_STATUS.UNAUTHORIZED_ACCESS    
        
        if (response.status_code == 400):
            return CTRL_STATUS.BAD_REQUEST
    
        if (response.status_code == 200):
            elemlist = json.loads(response.content).get('nodes').get('node')
            for elem in elemlist:
                if('id' in elem):
                    nlist.append(str(elem['id']))
        
        return (status, nlist)

    def get_all_nodes_conn_status(self):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
        nlist = [] 

        result = self.ctrl_get_request(url, self.adminName, self.adminPassword)
        status = result[0]
        if (status == CTRL_STATUS.CONN_ERROR):
            return status
       
        response = result[1]
        if (response.status_code == 401):
            return CTRL_STATUS.UNAUTHORIZED_ACCESS    
        
        if (response.status_code == 400):
            return CTRL_STATUS.BAD_REQUEST
    
        if (response.status_code == 200):
            elemlist = json.loads(response.content).get('nodes').get('node')            
            for elem in elemlist:
                if ('id' in elem):
                    nd = dict()
                    nd.update({'node' : elem['id']})
                    if (('netconf-node-inventory:connected' in elem) and
                        (elem['netconf-node-inventory:connected'] == True)):
                        nd.update({'connected' : True})
                    else:
                        nd.update({'connected' : False})
                    nlist.append(nd)
            
        return (status, nlist)

#================================
# KEEP
#================================
    def get_all_supported_schemas(self, nodeName):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:netconf-state/schemas"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName)
        slist = []
        
        result = self.ctrl_get_request(url, self.adminName, self.adminPassword)
        status = result[0]
        if (status == CTRL_STATUS.CONN_ERROR):
            return status
       
        response = result[1]
        if (response.status_code == 401):
            return CTRL_STATUS.UNAUTHORIZED_ACCESS    
        
        if (response.status_code == 400):
            return CTRL_STATUS.BAD_REQUEST
    
        if (response.status_code == 200):
            data = json.loads(response.content)
            elemlist = json.loads(response.content).get('schemas').get('schema')
            slist = data.get('schemas').get('schema')
        
        return (status, slist)



#================================
# TBD
#================================
    def get_schema(self, nodeName, schemaId, schemaVersion):
        templateUrl = "http://{}:{}/restconf/operations/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:get-schema"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName) 
        headers = {'content-type': 'application/yang.data+json', 'accept': 'text/json, text/html, application/xml, */*'}
        payload = {'input': {'identifier' : schemaId, 'version' : schemaVersion, 'format' : 'yang'}}
        schema = None

        result = self.ctrl_post_request(url, json.dumps(payload), headers, self.adminName, self.adminPassword)
        status = result[0]
        if (status != CTRL_STATUS.CONN_ERROR):
            response = result[1]
            if (response.status_code == 401):
                status = CTRL_STATUS.UNAUTHORIZED_ACCESS        
            elif (response.status_code == 400):
                status = CTRL_STATUS.BAD_REQUEST      
            elif (response.status_code == 200):
#                print response.headers.get('content-type')
                if(response.headers.get('content-type') == "application/xml"):
#                    print "XML content type"
                    doc = xmltodict.parse(response.content)
                    try:
                        tmp = doc['get-schema']['output']['data']
                        if(tmp):
                            schema = tmp
                            status = CTRL_STATUS.OK
                    except KeyError:
#                        print "error"
                        status = CTRL_STATUS.DATA_NOT_FOUND
                else:
                    print "TBD content type"
        
        return (status, schema)




def get_nodes_operational_datastore(ipAddr, portNum, uname, passwd, nodeId):
#    url="http://" + ipAddr + ":" + portNum + "/restconf/operational/opendaylight-inventory:nodes"
    url="http://{}:{}/restconf/operational/opendaylight-inventory:nodes".format(ipAddr, portNum)
    status = "Node is not connected"
    matchFound = False
    
    try:
        resp = requests.get(url, auth=HTTPBasicAuth(uname, passwd))    
    except ConnectionError:
        status = "HTTP server connection error"
        return status
    
    if (resp.status_code != 200):
        status = "HTTP request error %d" % resp.status_code
        return status
    
    data = json.loads(resp.content)
    nodes = data.get('nodes')
    nodes_list = nodes.get('node')
    for elem in nodes_list:
        print elem
        print type(elem)
        if ('id' in elem):
            print elem['id']
        if ('netconf-node-inventory:connected' in elem):
            print elem['netconf-node-inventory:connected']

    return status


#================================
# TBD
#================================
def get_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.iteritems():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found






