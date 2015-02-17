import string
import json

from framework.controller import STATUS
from framework.netconfnode import NetconfNode

#===============================================================================
# Class 'VRouter5600'
#===============================================================================
class VRouter5600(NetconfNode):
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, ctrl, name, ipAddr, portNum, adminName, adminPassword, tcpOnly=False):
        super(VRouter5600, self).__init__(ctrl, name, ipAddr, portNum, adminName, adminPassword, tcpOnly)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        return str(vars(self))

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_schemas(self):
        ctrl = self.ctrl
        myname = self.name
        result = ctrl.get_schemas(myname)
        return result

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_schema(self, schemaId, schemaVersion):
        ctrl = self.ctrl
        myname = self.name
        result = ctrl.get_schema(myname, schemaId, schemaVersion)
        return result

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_cfg(self):        
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)

        result = ctrl.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)

        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
       
        if (response.status_code == 200):
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
         
        return (status, response)
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_firewalls_cfg(self):        
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall"        
        modelref = templateModelRef       
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        url += modelref
        result = ctrl.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)

        if (response.status_code == 200):
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, response)
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_firewall_instance_cfg(self, instance):        
        templateModelRef = "vyatta-security:security/vyatta-security-firewall:firewall/name/{}"     
        modelref = templateModelRef.format(instance)
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_ext_mount_config_url(myname)
        url += modelref
        result = ctrl.http_get_request(url, data=None, headers=None)
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
            return (STATUS.HTTP_ERROR, None)
        
        return (status, response)
       
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def create_firewall_instance(self, fwInstance):        
        ctrl = self.ctrl
        myname = self.name

        url = ctrl.get_ext_mount_config_url(myname)
        headers = {'content-type': 'application/yang.data+json'}
        payload = fwInstance.get_payload()
        result = ctrl.http_post_request(url, payload, headers)
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
         
        return (status, response)
    
    #---------------------------------------------------------------------------
    # TBD
    #---------------------------------------------------------------------------
    def add_firewall_instance_rule(self, fwInstance, fwRule):
        pass
    
    #---------------------------------------------------------------------------
    # TBD
    #---------------------------------------------------------------------------
    def update_firewall_instance_rule(self, fwInstance, fwRule):
        pass
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def delete_firewall_instance(self, fwInstance):
        ctrl = self.ctrl
        myname = self.name

        url = ctrl.get_ext_mount_config_url(myname)
        ext = fwInstance.get_url_extension()
        url += ext
        rules = fwInstance.get_rules()
        for item in rules:
            name = item.get_name()
            result = ctrl.http_delete_request(url + "/name/" + name, data=None, headers=None)
            status = result[0]
            if (status == STATUS.CTRL_CONN_ERROR):
                break
            response = result[1]
            if (response == None):
                status = STATUS.CTRL_INTERNAL_ERROR
                break
            if (response.status_code == 200):
                status = STATUS.CTRL_OK
            else:
                print ("!!!Error, reason: %s" % response.reason)
                status = STATUS.HTTP_ERROR
                break
            
            return (status, None)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_dataplane_interface_inbound_firewall(self, ifName, fwName):
        ctrl = self.ctrl
        headers = {'content-type': 'application/yang.data+json'}
        url = ctrl.get_ext_mount_config_url(self.name)        
        obj = DataplaneInterfaceFirewall(ifName)
        obj.add_in_item(fwName)
        payload = obj.get_payload()
        urlext = obj.get_url_extension()
        result = ctrl.http_put_request(url + urlext, payload, headers)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)

        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200):
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, response)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def delete_dataplane_interface_firewall(self, ifName):        
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/{}/vyatta-security-firewall:firewall/"
        modelref = templateModelRef.format(ifName)
        myname = self.name
        ctrl = self.ctrl

        url = ctrl.get_ext_mount_config_url(myname)        
        result = ctrl.http_delete_request(url + modelref, data=None, headers=None)
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
        
        return (status, response)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_interfaces_cfg(self):        
        templateModelRef = "vyatta-interfaces:interfaces"        
        modelref = templateModelRef       
        ctrl = self.ctrl

        url = ctrl.get_ext_mount_config_url(self.name)
        url += modelref
        result = ctrl.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)
        
        if (response.status_code == 200):
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, response)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_dataplane_interfaces_list(self):        
        result = self.get_interfaces_cfg()
        status = result[0]
        dpIfList = []
        if (status == STATUS.CTRL_OK):
            response = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-dataplane:dataplane'
            if(p1 in response.content and p2 in response.content):
                items = json.loads(response.content).get(p1).get(p2)
                for item in items:
                    if 'tagnode' in item:
                        dpIfList.append(item['tagnode'])
        else:
            print ("!!!Error, reason: %s" % response.reason)
        
        return (status, dpIfList)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_dataplane_interfaces_cfg(self):
        result = self.get_interfaces_cfg()
        status = result[0]
        dpIfCfg = None
        if (status == STATUS.CTRL_OK):
            response = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-dataplane:dataplane'
            if(p1 in response.content and p2 in response.content):
                dpIfCfg = json.loads(response.content).get(p1).get(p2)
        else:
            print ("!!!Error, reason: %s" % response.reason)
        
        return (status, dpIfCfg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_dataplane_interface_cfg(self, ifName):        
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-dataplane:dataplane/{}"
        modelref = templateModelRef.format(ifName)
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(self.name)
        url += modelref

        result = ctrl.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)

        if (response.status_code == 200):
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, response)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_loopback_interfaces_list(self):        
        result = self.get_interfaces_cfg()
        status = result[0]
        lbInterfaces = []
        if (status == STATUS.CTRL_OK):
            response = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-loopback:loopback'
            if(p1 in response.content and p2 in response.content):
                items = json.loads(response.content).get(p1).get(p2)
                for item in items:
                    if 'tagnode' in item:
                        lbInterfaces.append(item['tagnode'])
        else:
            print ("!!!Error, reason: %s" % response.reason)
        
        return (status, lbInterfaces)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_loopback_interfaces_cfg(self):
        result = self.get_interfaces_cfg()
        status = result[0]
        lpIfCfg = None
        if (status == STATUS.CTRL_OK):
            response = result[1]
            p1 = 'interfaces'
            p2 = 'vyatta-interfaces-loopback:loopback'
            if(p1 in response.content and p2 in response.content):
                lpIfCfg = json.loads(response.content).get(p1).get(p2)
        else:
            print ("!!!Error, reason: %s" % response.reason)
        
        return (status, lpIfCfg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_loopback_interface_cfg(self, ifName):        
        templateModelRef = "vyatta-interfaces:interfaces/vyatta-interfaces-loopback:loopback/{}"
        modelref = templateModelRef.format(ifName)
        ctrl = self.ctrl
        url = ctrl.get_ext_mount_config_url(self.name)
        url += modelref

        result = ctrl.http_get_request(url, data=None, headers=None)
        status = result[0]
        if (status == STATUS.CTRL_CONN_ERROR):
            return (status, None)
        
        response = result[1]
        if (response == None):
            status = STATUS.CTRL_INTERNAL_ERROR
            return (status, None)

        if (response.status_code == 200):
                status = STATUS.CTRL_OK
        else:
            print ("!!!Error, reason: %s" % response.reason)
            status = STATUS.HTTP_ERROR
        
        return (status, response)
    
#===============================================================================
# 
#===============================================================================
class Firewall():
    mn1 = "vyatta-security:security"
    mn2 = "vyatta-security-firewall:firewall"
    def __init__(self):
        self.name = []
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        return str(vars(self))
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_payload(self):
        obj = json.loads(self.to_json())
        payload = {self.mn1:{self.mn2:obj}}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_name(self):
        return 
    def get_url_extension(self):
        return (self.mn1 + "/" +  self.mn2)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_rules(self, rules):
        self.name.append(rules)
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_rules(self):
        rules = []
        for item in self.name:
            rules.append(item)
        return rules

#===============================================================================
# Class 'Rules'
#===============================================================================
class Rules():
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, name):
        self.tagnode = name
        self.rule = []
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        return str(vars(self))
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_rule(self, rule):
        self.rule.append(rule)
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_name(self):
        return self.tagnode 

#===============================================================================
# Class 'Rule'
#===============================================================================
class Rule():
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, number):
        self.tagnode = number
        self.source = Object()
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        return str(vars(self))
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_action(self, action):
        self.action = action
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_source_address(self, srcAddr):
        self.source.address = srcAddr

#===============================================================================
# Class 'DataplaneInterfaceFirewall'
#===============================================================================
class DataplaneInterfaceFirewall():
    mn1 = "vyatta-interfaces:interfaces"
    mn2 = "vyatta-interfaces-dataplane:dataplane"
    mn3 = "vyatta-security-firewall:firewall"

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, ifName):
        self.tagnode = ifName
        self.firewall = Object()
        self.firewall.inlist = []
        self.firewall.outlist = []
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_in_item(self, name):
        self.firewall.inlist.append(name)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_out_item(self, name):
        self.firewall.outlist.append(name)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_url_extension(self):
        return (self.mn1 + "/" + self.mn2 + "/" +  self.tagnode)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_name(self):
        return self.tagnode
     
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_payload(self):        
        s = self.to_json()
        s = string.replace(s, 'firewall', self.mn3)
        s = string.replace(s, 'inlist', "in")
        s = string.replace(s, 'outlist', "out")
        obj = json.loads(s)
        payload = {self.mn2:obj}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)

#===============================================================================
# Class 'Object'
#===============================================================================
class Object():
    pass
        