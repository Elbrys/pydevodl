import json
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, Timeout
import xmltodict

from framework.netconfnode import  *

#===============================================================================
# KEEP
#===============================================================================
def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

STATUS = enum('CTRL_OK', 'CTRL_CONN_ERROR', 'CTRL_DATA_NOT_FOUND', 'CTRL_BAD_REQUEST',
              'CTRL_UNAUTHORIZED_ACCESS', 'CTRL_INTERNAL_ERROR',
              'NODE_CONNECTED', 'NODE_DISONNECTED', 'NODE_NOT_FOUND', 'NODE_CONFIGURED',                   
              'HTTP_ERROR', 'N_A')

#===============================================================================
# KEEP
#===============================================================================
class Status(object):
    def __init__(self, status):
        if status not in (STATUS.CTRL_OK,
                          STATUS.CTRL_CONN_ERROR,
                          STATUS.CTRL_DATA_NOT_FOUND,
                          STATUS.CTRL_BAD_REQUEST,
                          STATUS.CTRL_UNAUTHORIZED_ACCESS,
                          STATUS.CTRL_INTERNAL_ERROR,
                          STATUS.NODE_CONNECTED,
                          STATUS.NODE_DISONNECTED,
                          STATUS.NODE_NOT_FOUND,
                          STATUS.NODE_CONFIGURED,
                          STATUS.HTTP_ERROR,
                          STATUS.N_A
                          ):
            raise ValueError('undefined status value')
        self.status = status
    
    def string(self):
        if (self.status == STATUS.CTRL_OK):
            return "success"
        elif( self.status == STATUS.CTRL_CONN_ERROR):
            return "server connection error"
        elif( self.status == STATUS.CTRL_DATA_NOT_FOUND):
            return "requested data not found"
        elif( self.status == STATUS.CTRL_BAD_REQUEST):
            return "bad or invalid data in request"
        elif( self.status == STATUS.CTRL_UNAUTHORIZED_ACCESS):
            return "server unauthorized access"
        elif( self.status == STATUS.CTRL_INTERNAL_ERROR):
            return "Internal Server Error"        
        elif( self.status == STATUS.NODE_CONNECTED):
            return "node is connected"
        elif( self.status == STATUS.NODE_DISONNECTED):
            return "node is disconnected"
        elif( self.status == STATUS.NODE_NOT_FOUND):
            return "node not found"
        elif( self.status == STATUS.NODE_CONFIGURED):
            return "node is configured"
        elif( self.status == STATUS.HTTP_ERROR):
            return "HTTP error"
        elif( self.status == STATUS.N_A):
            return "unknown error"
        else:
            print ("Error: undefined status value %s" % self.status)
            raise ValueError('!!!undefined status value')

#===============================================================================
# KEEP
#===============================================================================
class Controller():
    def __init__(self, ipAddr, portNum, adminName, adminPassword, timeout=5):
        self.ipAddr = ipAddr
        self.portNum = portNum
        self.adminName = adminName
        self.adminPassword = adminPassword
        self.timeout = timeout
#        self.nodes = []
    '''
    def add_node(self,node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes
    
    def get_node(self, nodeName):
        node = None
        for item in self.nodes:
            if(isinstance(item, NetconfNode) and item.name == nodeName):
                node = item
                break
        return node
    '''
    
    def to_string(self):
        return str(vars(self))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def http_get_request(self, url, data, headers):
        resp = None
        status = None
        try:
            resp = requests.get(url,
                                auth=HTTPBasicAuth(self.adminName, self.adminPassword), 
                                data=data, headers=headers, timeout=self.timeout)
            status = STATUS.CTRL_OK
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)
            status = STATUS.CTRL_CONN_ERROR
        
        return (status, resp)
    
    def http_post_request(self, url, data, headers):
        resp = None
        status = None
        try:
            resp = requests.post(url,
                                 auth=HTTPBasicAuth(self.adminName, self.adminPassword),
                                 data=data, headers=headers, timeout=self.timeout)
            status = STATUS.CTRL_OK
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)
            status = STATUS.CTRL_CONN_ERROR
        
        return (status, resp)

    def http_put_request(self, url, data, headers):
        resp = None
        status = None
        try:
            resp = requests.put(url,
                                auth=HTTPBasicAuth(self.adminName, self.adminPassword),
                                data=data, headers=headers, timeout=self.timeout)
            status = STATUS.CTRL_OK
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)
            status = STATUS.CTRL_CONN_ERROR
        
        return (status, resp)
    
    def http_delete_request(self, url, data, headers):
        resp = None
        status = None
        try:
            resp = requests.delete(url,
                                   auth=HTTPBasicAuth(self.adminName, self.adminPassword),
                                   data=data, headers=headers, timeout=self.timeout)
            status = STATUS.CTRL_OK
        except (ConnectionError, Timeout) as e:
            print "Error: " + repr(e)
            status = STATUS.CTRL_CONN_ERROR
        
        return (status, resp)
    
    def check_node_config_status(self, nodeId):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
        
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return status
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return status
        
        if (response.status_code == 200):
            status = STATUS.NODE_NOT_FOUND
            if("nodes" in response.content and "node" in response.content):
                itemlist = json.loads(response.content).get('nodes').get('node')
                for item in itemlist:
                    if(item['id'] == nodeId):
                        status = STATUS.NODE_CONFIGURED
                        break
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return status
    
    def check_node_conn_status(self, nodeId):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
           
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return status
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return status
        
        if (response.status_code == 200):
            status = STATUS.NODE_NOT_FOUND            
            if("nodes" in response.content and "node" in response.content):            
                itemlist = json.loads(response.content).get('nodes').get('node')            
                for item in itemlist:
                    if('id' in item and item['id'] == nodeId):
                        status = STATUS.NODE_DISONNECTED
                        if (('netconf-node-inventory:connected' in item) and
                            (item['netconf-node-inventory:connected'] == True)):
                            status = STATUS.NODE_CONNECTED                        
                            break
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR

        return status

    def get_all_nodes_in_config(self):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)        
        nlist = [] 
        
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("nodes" in response.content and "node" in response.content):
                elemlist = json.loads(response.content).get('nodes').get('node')
                for elem in elemlist:
                    if('id' in elem):
                        nlist.append(str(elem['id']))
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR

        return (status, nlist)

    def get_all_nodes_conn_status(self):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes"
        url = templateUrl.format(self.ipAddr, self.portNum)
        nlist = [] 

        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND           
            if("nodes" in response.content and "node" in response.content):            
                itemlist = json.loads(response.content).get('nodes').get('node')
                status = STATUS.CTRL_OK
                for item in itemlist:
                    if ('id' in item):
                        nd = dict()
                        nd.update({'node' : item['id']})
                        if (('netconf-node-inventory:connected' in item) and
                            (item['netconf-node-inventory:connected'] == True)):
                            nd.update({'connected' : True})
                        else:
                            nd.update({'connected' : False})
                        nlist.append(nd)
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR

        return (status, nlist)

    def get_schemas(self, nodeName):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:netconf-state/schemas"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName)
        slist = None
        
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("schemas" in response.content and "chema" in response.content):            
                status = STATUS.CTRL_OK
                data = json.loads(response.content).get('schemas').get('schema')
                slist = data
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, slist)

    def get_schema(self, nodeName, schemaId, schemaVersion):
        templateUrl = "http://{}:{}/restconf/operations/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:get-schema"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName) 
        headers = {'content-type': 'application/yang.data+json', 'accept': 'text/json, text/html, application/xml, */*'}
        payload = {'input': {'identifier' : schemaId, 'version' : schemaVersion, 'format' : 'yang'}}
        schema = None

        result = self.http_post_request(url, json.dumps(payload), headers)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if(response.headers.get('content-type') == "application/xml"):
                doc = xmltodict.parse(response.content)
                try:
                    schema = doc['get-schema']['output']['data']
                    status = STATUS.CTRL_OK
                except (KeyError) as e:
                    print "Error: " + repr(e)
            else:
                print "TBD: not implemented content type parser"
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR

        return (status, schema)

    def get_netconf_operations(self, nodeName):
        templateUrl = "http://{}:{}/restconf/operations/opendaylight-inventory:nodes/node/{}/yang-ext:mount/"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName) 
        olist = None

        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("operations" in response.content):
                olist = json.loads(response.content).get('operations')
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, olist)

    def get_all_modules_operational_state(self):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules"
        url = templateUrl.format(self.ipAddr, self.portNum)
        mlist = None

        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)

        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("modules" in response.content and "module" in response.content):             
                mlist = json.loads(response.content).get('modules').get('module')
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR    
        
        return (status, mlist)

    #---------------------------------------------------------------------------
    # KEEP
    #---------------------------------------------------------------------------
    def get_module_operational_state(self, moduleType, moduleName):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules/module/{}/{}"              
        url = templateUrl.format(self.ipAddr, self.portNum, moduleType, moduleName)         
        module = None

        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)

        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
       
        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("module" in response.content):
                module = json.loads(response.content).get('module')
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, module)

    #---------------------------------------------------------------------------
    # KEEP
    #---------------------------------------------------------------------------
    def get_sessions_info(self, nodeName):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/{}/yang-ext:mount/ietf-netconf-monitoring:netconf-state/sessions"
        url = templateUrl.format(self.ipAddr, self.portNum, nodeName)
        slist = None
        
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
 
        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("sessions" in response.content):
                slist = json.loads(response.content).get('sessions')
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, slist)

    #---------------------------------------------------------------------------
    # KEEP
    #---------------------------------------------------------------------------
    def get_streams_info(self):
        templateUrl = "http://{}:{}/restconf/streams"        
        url = templateUrl.format(self.ipAddr, self.portNum)
        slist = None
        
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)

        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("streams" in response.content):
                slist = json.loads(response.content).get('streams')
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, slist)

    #---------------------------------------------------------------------------
    # KEEP
    #---------------------------------------------------------------------------
    def get_service_providers_info(self):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:services"        
        url = templateUrl.format(self.ipAddr, self.portNum)
        slist = None
        
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)

        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("services" in response.content and "service" in response.content):
                slist = json.loads(response.content).get('services').get('service')
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR    
        
        return (status, slist)
    
    #---------------------------------------------------------------------------
    # KEEP
    #---------------------------------------------------------------------------
    def get_service_provider_info(self, name):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:services/service/{}"
        url = templateUrl.format(self.ipAddr, self.portNum, name)         
        service = None
        
        result = self.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
       
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)

        if (response.status_code == 200):
            status = STATUS.CTRL_DATA_NOT_FOUND
            if("service" in response.content):
                service = json.loads(response.content).get('service')
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR    
        
        return (status, service)

    #---------------------------------------------------------------------------
    # KEEP
    #---------------------------------------------------------------------------
    def add_netconf_node(self, node):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules"        
        xmlPayloadTemplate = '''
        <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
          <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
          <name>{}</name>
          <address xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</address>
          <port xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</port>
          <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</username>
          <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</password>
          <tcp-only xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</tcp-only>
          <event-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
            <name>global-event-executor</name>
          </event-executor>
          <binding-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
            <name>binding-osgi-broker</name>
          </binding-registry>
          <dom-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
            <name>dom-broker</name>
          </dom-registry>
          <client-dispatcher xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
            <name>global-netconf-dispatcher</name>
          </client-dispatcher>
          <processing-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
            <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">prefix:threadpool</type>
            <name>global-netconf-processing-executor</name>
          </processing-executor>
        </module>
        '''
        payload = xmlPayloadTemplate.format(node.name, node.ipAddr, node.portNum, node.adminName, node.adminPassword, node.tcpOnly)
        url = templateUrl.format(self.ipAddr, self.portNum)
        headers = {'content-type': 'application/xml', 'accept': 'application/xml'}
        result = self.http_post_request(url, payload, headers)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)

        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        response = result[1]
        if (response.status_code == 200 or response.status_code == 204):
            status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, None)

    #---------------------------------------------------------------------------
    # KEEP
    #---------------------------------------------------------------------------
    def delete_netconf_node(self, netconfdev):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/{}"
        url = templateUrl.format(self.ipAddr, self.portNum, netconfdev.name)

        result = self.http_delete_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200 or response.status_code == 204):
            status = STATUS.CTRL_OK                        
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, None)
        
    #---------------------------------------------------------------------------
    # TBD: 
    # NOTE: It is unclear what NETCONF node attributes are allowed for dynamic
    #       configuration changes. For now we just follow example published
    #       on ODL wiki:
    #       https://wiki.opendaylight.org/view/OpenDaylight_Controller:Config:Examples:Netconf
    #---------------------------------------------------------------------------
    def modify_netconf_node_in_config(self, netconfdev):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules"      
        url = templateUrl.format(self.ipAddr, self.portNum)
        xmlPayloadTemplate = '''
        <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
          <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
          <name>{}</name>
          <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</username>
          <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</password>
        </module>
        '''
        payload = xmlPayloadTemplate.format(netconfdev.devName, netconfdev.adminName, netconfdev.adminPassword)
        headers = {'content-type': 'application/xml', 'accept': 'application/xml'}
        result = self.http_post_request(url, payload, headers)                
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)

        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200 or response.status_code == 204):
            status = STATUS.CTRL_OK                        
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, None)
        
    def get_ext_mount_config_url(self, node):
        templateUrl = "http://{}:{}/restconf/config/opendaylight-inventory:nodes/node/{}/yang-ext:mount/"
        url = templateUrl.format(self.ipAddr, self.portNum, node)
        return url    

    def get_ext_mount_operational_url(self, node):
        templateUrl = "http://{}:{}/restconf/operational/opendaylight-inventory:nodes/node/{}/yang-ext:mount/"
        url = templateUrl.format(self.ipAddr, self.portNum, node)
        return url    


'''
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
'''
