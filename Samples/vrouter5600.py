'''
Created on Feb 3, 2015

@author: sergei
'''

import requests
from requests.auth import HTTPBasicAuth
import json

from controller import *
from netconfdev import *

#================================
# KEEP
#================================
class VRouter5600(NetconfDevice):
    def __init__(self, controller, netconfdev):
        self.controller = controller
        self.node = netconfdev
    
    def to_string(self):
#        attrs = vars(self.common)
        ctrl = vars(self.controller)
        node = vars(self.node)
#        print attrs
#        print ', '.join("%s: %s" % item for item in attrs.items())
#        print ("devName %s" % self.common.devName)
#        print ("ipAddr %s" % self.common.ipAddr)
#        print ("portNum %s" % self.common.portNum)
#        print ("adminName %s" % self.common.adminName)
#        print ("adminPassword %s" % self.common.adminPassword)
#        return (ctrl, node)
#        return str(vars(self.controller)) + str(vars(self.node))
        return str(vars(self.node))

#================================
# KEEP
#================================
    def get_schemas(self):
        ctrl = self.controller
        myname = self.node.devName
        result = ctrl.get_all_supported_schemas(myname)
        return result
        '''
        ctrl.get_url()
        ns = "vyatta-security:security/vyatta-security-firewall:firewall"
        
        "curl -u admin:admin -v http://172.22.18.245:8080/restconf/operational/opendaylight-inventory:nodes/node/vRouter/yang-ext:mount/ietf-netconf-monitoring:netconf-state/schemas/ | python -mjson.tool"
        '''
#================================
# KEEP
#================================
    def get_schema(self, schemaId, schemaVersion):
        ctrl = self.controller
        myname = self.node.devName
        result = ctrl.get_schema(myname, schemaId, schemaVersion)
        return result
        
    def get_firewall_all_cfg(self):        
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall"        
        modelref = templateModelRef       
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
        result = ctrl.ctrl_get_request(url + modelref)
        return result
        
    def get_firewall_instance_cfg(self, instance):        
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall/name/{}"     
        modelref = templateModelRef.format(instance)
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
#        print url + modelref
        result = ctrl.ctrl_get_request(url + modelref)
        
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response.status_code == 401):
            return (STATUS.CTRL_UNAUTHORIZED_ACCESS, None)
        
        if (response.status_code == 400):
            return (STATUS.CTRL_BAD_REQUEST, None)

        if (response.status_code == 404):
            return (STATUS.CTRL_DATA_NOT_FOUND, None)
    
        if (response.status_code == 200 or response.status_code == 204):
            status = STATUS.CTRL_OK        
#        print "+++++++++"
#        print (status, response)
        return (status, response)

        
#================================
# TBD
#================================
    def create_firewall_instance_cfg(self, name):        
#        templateModelRef = ""     
#        modelref = templateModelRef
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
        headers = {'content-type': 'application/yang.data+json'}
        
        topmodel = "vyatta-security:security"
        thismodel = "vyatta-security-firewall:firewall"
        address = "172.22.17.108"
        groupName = name
        ruleNumber = 77
        payload = {
          topmodel:
          {
             thismodel:
             {
                "name": [
                    {
                        "tagnode": groupName,
                        "rule": [
                            {
                                "action": "accept",
                                "source": {
                                    "address": address
                                },
                                "tagnode": ruleNumber
                            }
                        ]
                    }
                ]
             }
           }
        }
#        payload = {topmodel:{thismodel:{"name": [{"rule": [{"tagnode": ruleNumber, "action": "accept","source": {"address": address}}],"tagnode": fwGroupName}]}}}
#        print url
#        print headers
        result = ctrl.ctrl_post_request(url, json.dumps(payload), headers)
#        print result
        return result
        
#================================
# KEEP
#================================
    def delete_firewall_instance_cfg(self, name):
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall/name/{}"
        modelref = templateModelRef.format(name)
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
#        print url + modelref
        result = ctrl.ctrl_delete_request(url + modelref)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response.status_code == 401):
            return (STATUS.CTRL_UNAUTHORIZED_ACCESS, None)
        
        if (response.status_code == 400):
            return (STATUS.CTRL_BAD_REQUEST, None)
    
        if (response.status_code == 200 or response.status_code == 204):
            status = STATUS.CTRL_OK
        
#        print (status, response)
        return (status, response)









#================================
# TBD
#================================
    def apply_firewall_instance_to_interface(self, ifName, fwInstanceName):        
#        templateModelRef = ""     
#        modelref = templateModelRef
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
        headers = {'content-type': 'application/yang.data+json'}
        
        print ("+++ name: " + ifName)
        print ("+++ headers: " + str(headers))
        print ("+++ url: " + url)
        topmodel = "vyatta-interfaces:interfaces"
        thismodel = "vyatta-interfaces-dataplane:dataplane"
        fwmodel = "vyatta-security-firewall:firewall"
        payload = {
          thismodel:
          {
            "tagnode": ifName,
            fwmodel: {
                "in": [
                    fwInstanceName
                 ]
            }
          }
        }
        print ("+++ payload: " + str(payload))
        print ("+++ json: " + json.dumps(payload, sort_keys=True, indent=4))
        url1 = url + topmodel + "/" + thismodel + "/" + ifName
        print ("+++url1: " + url1)
        result = ctrl.ctrl_put_request(url1, json.dumps(payload), headers)
        print result
        
#================================
# TBD
#================================
    def delete_firewall_from_interface(self, ifName):        
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/{}/vyatta-security-firewall:firewall/"
        modelref = templateModelRef.format(ifName)
        myname = self.node.devName
        ctrl = self.controller
        url = ctrl.get_ext_mount_cfg_url(myname)
        print ("+++ url: " + url)
        print ("+++ modelref: " + modelref)
        print ("+++ both: " + url + modelref)
        
        result = ctrl.ctrl_delete_request(url + modelref)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response.status_code == 401):
            return (STATUS.CTRL_UNAUTHORIZED_ACCESS, None)
        
        if (response.status_code == 400):
            return (STATUS.CTRL_BAD_REQUEST, None)
    
        if (response.status_code == 200 or response.status_code == 204):
            status = STATUS.CTRL_OK
        
        print (status, response)
        return (status, response)


#http://172.22.18.186:8080/restconf/config/opendaylight-inventory:nodes/node/vRouter/yang-ext:mount/vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/dp0p1p7/vyatta-security-firewall:firewall/

#   def delete_firewall_from_interface(self, ifName, fwInstanceName):        
#




#================================
# TBD
#================================
    def create_firewall_instance(self, fwInstance):        
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
        print url
        headers = {'content-type': 'application/yang.data+json'}
        print headers
        payload = fwInstance.get_payload()
        print payload
#        ext = fwInstance.get_url_extension()
#        print ext
#        url += ext
#        print url
        result = ctrl.ctrl_post_request(url, payload, headers)
#        print result[1].content
        return result


class Firewall():
    mn1 = "vyatta-security:security"
    mn2 = "vyatta-security-firewall:firewall"
    def __init__(self):
        self.name = []
    def to_string(self):
        return str(vars(self))
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 
    def get_payload(self):
        obj = json.loads(self.to_json())
        payload = {self.mn1:{self.mn2:obj}}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def get_url_extension(self):
        return (self.mn1 + "/" +  self.mn2)
    def add_rules(self, rules):
        self.name.append(rules)    

class Rules():
    def __init__(self, name):
        self.tagnode = name
        self.rule = []
    def to_string(self):
        return str(vars(self))
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def add_rule(self, rule):
        self.rule.append(rule)

class Rule():
    def __init__(self, number):
        self.tagnode = number
        self.source = Object()
    def to_string(self):
        return str(vars(self))
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def add_action(self, action):
        self.action = action
    def add_source_address(self, srcAddr):
        self.source.address = srcAddr

       
class Object():
    pass














        
        
'''
        payload = {
          "vyatta-security:security":
          {
             "vyatta-security-firewall:firewall":
             {
                "name": [
                    {
                        "rule": [
                            {
                                "action": "accept",
                                "source": {
                                    "address": "172.22.17.108"
                                },
                                "tagnode": 1
                            }
                        ],
                        "tagnode": fwName
                    }
                ]
             }
           }
        }
'''
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        