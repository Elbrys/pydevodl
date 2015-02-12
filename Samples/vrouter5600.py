import requests
from requests.auth import HTTPBasicAuth
import json
import string

from controller import *
from netconfdev import *

#================================
# KEEP
#================================
class VRouter5600(NetconfDevice):
    def __init__(self, controller, node):
        self.controller = controller
        self.node = node
    
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
# KEEP
#================================
    def apply_firewall_to_dataplane_interface(self, dpIfFwObj):        
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
        headers = {'content-type': 'application/yang.data+json'}        
        payload = dpIfFwObj.get_payload()
        urlext = dpIfFwObj.get_url_extension()
        url += urlext
        result = ctrl.ctrl_put_request(url, payload, headers)
        return result
        
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

#================================
# KEEP
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

#================================
# KEEP
#================================
    def delete_firewall_instance(self, fwInstance):
        ctrl = self.controller
        myname = self.node.devName
        url = ctrl.get_ext_mount_cfg_url(myname)
        headers = {'content-type': 'application/yang.data+json'}
#        print headers
        ext = fwInstance.get_url_extension()
        url += ext
#        print url
        rules = fwInstance.get_rules()
#        print rules
        for item in rules:
            name = item.get_name()
#            print(url + "/name/" + name)
            result = ctrl.ctrl_delete_request(url + "/name/" + name)
            status = result[0]
            if(status != STATUS.CTRL_OK):
                break

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
        
    def get_rules(self):
        rules = []
        for item in self.name:
            rules.append(item)
        return rules

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
        
    def get_name(self):
        return self.tagnode 

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


class InterfaceDataplane(VRouter5600):
    mn1 = "vyatta-interfaces:interfaces"
    mn2 = "vyatta-interfaces-dataplane:dataplane"
    mn3 = "vyatta-security-firewall:firewall"
    def __init__(self, vrouter, name):
#        self.vrouter = vrouter
        self.tagnode = name
        self.firewall = None
#        self.firewall = InterfaceDataplaneFirewall("in", "out")
    
    '''
    def jdefault(self, o):
        print "xxx"
        print type(o.__dict__)
#        for item in o.__dict__.items():
#            print item
        r = dict(o.__dict__)        
#        if r['vrouter']:
#            print "@@@@@@@"
#            del(r['vrouter'])
        for item in r.items():
            print item

        return o.__dict__
    '''
    
    def to_string(self):
        return str(vars(self))
    
    def to_json(self):
#        return json.dumps(self, default=self.jdefault, sort_keys=True, indent=4)
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def get_payload(self):        
        s = self.to_json()
        s = string.replace(s, 'firewall', self.mn3)
        s = string.replace(s, 'inlist', "in")
        s = string.replace(s, 'outlist', "out")
        
        obj = json.loads(s)
        payload = {self.mn2:obj}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)
#        return payload
    
    def add_firewall(self, firewall):
        self.firewall = firewall
#        payload = {self.mn2:{self.tagnode, self.mn3}}
#        payload = {self.mn2}
#        print payload
#        print json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def apply_in_firewall(self, inFw):
#        self.inlist.append(inFw)
        obj = InterfaceDataplaneFirewall()
        obj.inlist.append(inFw)
#        self.firewall.append(obj)
        self.firewall = obj
        payload = self.get_payload()
        print payload
#        ctrl = self.vrouter.controller
        headers = {'content-type': 'application/yang.data+json'}
#        url = ctrl.get_ext_mount_cfg_url(self.tagnode)
#        print url
#        result = ctrl.ctrl_put_request(url, payload, headers)
    

class InterfaceDataplaneFirewall():
     mn1 = "vyatta-interfaces:interfaces"
     mn2 = "vyatta-interfaces-dataplane:dataplane"
     mn3 = "vyatta-security-firewall:firewall"
     def __init__(self, ifName):
        self.tagnode = ifName
        inlist = []
        outlist = []
        self.firewall = Object()
        self.firewall.inlist = []
        self.firewall.outlist = []
        
     def add_in_item(self, name):
        self.firewall.inlist.append(name)

     def add_out_item(self, name):
        self.firewall.outlist.append(name)
    
     def to_json(self):
#        s = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
#        s = string.replace(s, 'inlist', "in")
#        s = string.replace(s, 'outlist', "out")
#        obj = json.loads(s)
#        return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

     def get_url_extension(self):
        return (self.mn1 + "/" + self.mn2 + "/" +  self.tagnode)

     def get_name(self):
         return self.tagnode
     
     def get_payload(self):        
        s = self.to_json()
        s = string.replace(s, 'firewall', self.mn3)
        s = string.replace(s, 'inlist', "in")
        s = string.replace(s, 'outlist', "out")
        
        obj = json.loads(s)
        payload = {self.mn2:obj}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    
     '''
     def get_payload(self):        
        s = self.to_json()
        s = string.replace(s, 'firewall', self.mn3)
        s = string.replace(s, 'inlist', "in")
        s = string.replace(s, 'outlist', "out")        
        obj = json.loads(s)
        payload = {self.mn2:obj}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    '''
   

class Object():
    pass
        