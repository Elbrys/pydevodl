import json
import string

from framework.controller import STATUS
from framework.netconfnode import  *

#================================
# KEEP
#================================
class VRouter5600(NetconfNode):
    def __init__(self, ctrl, name, ipAddr, portNum, adminName, adminPassword, tcpOnly=False):
        super(VRouter5600, self).__init__(ctrl, name, ipAddr, portNum, adminName, adminPassword, tcpOnly)
    
    def to_string(self):
        return str(vars(self))

#================================
# KEEP
#================================
    def get_schemas(self):
        ctrl = self.ctrl
        myname = self.name
        result = ctrl.get_all_supported_schemas(myname)
        return result

#================================
# KEEP
#================================
    def get_schema(self, schemaId, schemaVersion):
        ctrl = self.ctrl
        myname = self.name
        result = ctrl.get_schema(myname, schemaId, schemaVersion)
        return result
        
    def get_firewall_cfg(self):        
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall"        
        modelref = templateModelRef       
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        result = ctrl.http_get_request(url + modelref)
        return result
        
    def get_firewall_instance_cfg(self, instance):        
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall/name/{}"     
        modelref = templateModelRef.format(instance)
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
#        print url + modelref
        result = ctrl.http_get_request(url + modelref)
        
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
        return (status, response)
       
#================================
# KEEP
#================================
    def apply_firewall_to_dataplane_interface(self, dpIfFwObj):        
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        headers = {'content-type': 'application/yang.data+json'}        
        payload = dpIfFwObj.get_payload()
        urlext = dpIfFwObj.get_url_extension()
        url += urlext
        result = ctrl.http_put_request(url, payload, headers)
        return result
        
#================================
# TBD
#================================
    def delete_firewall_from_interface(self, ifName):        
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/{}/vyatta-security-firewall:firewall/"
        modelref = templateModelRef.format(ifName)
        myname = self.name
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(myname)
#        print ("+++ url: " + url)
#        print ("+++ modelref: " + modelref)
#        print ("+++ both: " + url + modelref)
        
        result = ctrl.http_delete_request(url + modelref)
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
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
#        print url
        headers = {'content-type': 'application/yang.data+json'}
#        print headers
        payload = fwInstance.get_payload()
#        print payload
#        ext = fwInstance.get_url_extension()
#        print ext
#        url += ext
#        print url
        result = ctrl.http_post_request(url, payload, headers)
#        print result[1].content
        return result

#================================
# KEEP
#================================
    def delete_firewall_instance(self, fwInstance):
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
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
            result = ctrl.http_delete_request(url + "/name/" + name)
            status = result[0]
            if(status != STATUS.CTRL_OK):
                break

        return result

#================================
# KEEP
#================================
    def get_interfaces_cfg(self):        
        templateModelRef = "vyatta-interfaces:interfaces"        
        modelref = templateModelRef       
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(self.name)
        print url + modelref
        result = ctrl.http_get_request(url + modelref)
        print result
        return result

#================================
# KEEP
#================================
    def get_dataplane_interface_cfg(self, ifName):        
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/{}"
        modelref = templateModelRef.format(ifName)
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(self.name)
        print url + modelref
        result = ctrl.http_get_request(url + modelref)
        print result
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
        self.tagnode = name
        self.firewall = None
       
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
    
    def add_firewall(self, firewall):
        self.firewall = firewall

    def apply_in_firewall(self, inFw):
        obj = InterfaceDataplaneFirewall()
        obj.inlist.append(inFw)
        self.firewall = obj
        payload = self.get_payload()
        print payload
        headers = {'content-type': 'application/yang.data+json'}
#        url = ctrl.get_ext_mount_cfg_url(self.tagnode)
#        print url
#        result = ctrl.http_put_request(url, payload, headers)
    

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

class Object():
    pass
        