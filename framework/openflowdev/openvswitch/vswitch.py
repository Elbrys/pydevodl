
import json
import string
#import collections

from collections import OrderedDict

from framework.controller.openflownode import OpenflowNode
from framework.common.status import OperStatus, STATUS
from framework.common.utils import find_key_values_in_dict
from framework.common.utils import replace_str_value_in_dict
from framework.common.utils import find_key_value_in_dict
from framework.common.utils import find_dict_in_list


class VSwitch(OpenflowNode):
    """Class that represents an instance of 'Open vSwitch' (OpenFlow capable device)."""
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, ctrl=None, name=None, dpid=None):
        """Initializes this object properties."""
        super(VSwitch, self).__init__(ctrl, name)
        self.dpid = dpid
        self.ports=[]

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        """Returns string representation of this object."""
        return str(vars(self))

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        """Returns JSON representation of this object."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_switch_info(self):        
        status = OperStatus()
        info = {}
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_node_operational_url(myname)
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            dictionary = json.loads(resp.content)
            p1 = 'node'
            if (p1 in dictionary):
                p2 = 'flow-node-inventory:manufacturer'
                vlist = find_key_values_in_dict(dictionary, p2)
                if (len(vlist) != 0):
                    info['manufacturer'] = vlist[0]
                
                p3 = 'flow-node-inventory:serial-number'
                vlist = find_key_values_in_dict(dictionary, p3)
                if (len(vlist) != 0):
                    info['serial-number'] = vlist[0]
                
                p4 = 'flow-node-inventory:software'
                vlist = find_key_values_in_dict(dictionary, p4)
                if (len(vlist) != 0):
                    info['software'] = vlist[0]
                
                p5 = 'flow-node-inventory:hardware'
                vlist = find_key_values_in_dict(dictionary, p5)
                if (len(vlist) != 0):
                    info['hardware'] = vlist[0]
                
                p6 = 'flow-node-inventory:description'
                vlist = find_key_values_in_dict(dictionary, p6)
                if (len(vlist) != 0):
                    info['description'] = vlist[0]
                
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, info)
        
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_features_info(self):        
        status = OperStatus()
        info = {}
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_node_operational_url(myname)
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            dictionary = json.loads(resp.content)
            p2 = 'flow-node-inventory:switch-features'
            vlist = find_key_values_in_dict(dictionary, p2)
            if (len(vlist) != 0 and (type(vlist[0]) is dict)):
                p3 = 'flow-node-inventory:flow-feature-capability-'
                info = replace_str_value_in_dict(vlist[0], p3, '')
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, info)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_ports_info(self):        
        status = OperStatus()
        info = []
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_node_operational_url(myname)
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            dictionary = json.loads(resp.content)
            p2 = 'node-connector'
            vlist = find_key_values_in_dict(dictionary, p2)
            if (len(vlist) != 0 and (type(vlist[0]) is list)):
                try:
                    for item in vlist[0]:
                        port = {}
                        port['id'] = item['id']
                        port['number'] = item['flow-node-inventory:port-number']
                        port['name'] = item['flow-node-inventory:name']
                        port['MAC address'] = item['flow-node-inventory:hardware-address']
                        s = item['flow-node-inventory:current-feature']
                        port['current feature'] = s.upper()
                        info.append(port)
                    status.set_status(STATUS.OK)
                except () as e:
                    print "Error: " + repr(e)
                    status.set_status(STATUS.DATA_NOT_FOUND)
            else:
                print "---------------"
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, info)


    def get_port_info(self, portnum):
        status = OperStatus()
        info = {}
        templateUrlExt = "/node-connector/{}:{}"
        urlext = templateUrlExt.format(self.name, portnum)
        ctrl = self.ctrl
        url = ctrl.get_node_operational_url(self.name)
        url += urlext
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            dictionary = json.loads(resp.content)
            try:
                vlist = dictionary['node-connector']
                if (len(vlist) != 0 and (type(vlist[0]) is dict)):
                    info = vlist[0]
                    status.set_status(STATUS.OK)
                else:
                    status.set_status(STATUS.DATA_NOT_FOUND)
            except () as e:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, info)
    
    def get_flows(self, tableid):
        status = OperStatus()
        flows = {}
        templateUrlExt = "/flow-node-inventory:table/{}"
        urlext = templateUrlExt.format(tableid)
        ctrl = self.ctrl
        url = ctrl.get_node_operational_url(self.name)
        url += urlext
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            dictionary = json.loads(resp.content)
            try:
                vlist = dictionary['flow-node-inventory:table']
                if (len(vlist) != 0 and (type(vlist[0]) is dict) and ('flow' in vlist[0])):
                    flows = vlist[0]['flow']
                    status.set_status(STATUS.OK)
                else:
                    status.set_status(STATUS.DATA_NOT_FOUND)
            except () as e:
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, flows)

    def get_flows_ovs_syntax(self, tableid, sort=None):
        ovsflows = []
        result = self.get_flows(tableid)
        status = result[0]
        if(status.eq(STATUS.OK) == True):
            flist = result[1]
            if (sort == True):
                flist.sort(key=self.__getPriorityKey)                
            for item in flist:
                f = self.odl_to_ovs_flow_syntax(item)
                ovsflows.append(f)

        return (status, ovsflows)
        
    def odl_to_ovs_flow_syntax(self, odlflow):
        od = OrderedDict()
#        print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")        
        f = odlflow
        
        v = find_key_value_in_dict(f, 'cookie')
        if (v != None):
            od['cookie'] = hex(v)

        v = find_key_value_in_dict(f, 'duration')
        if (v != None and type(v) is dict):
            if ('second' in v and 'nanosecond' in v):
                s = v['second']
                ns = v['nanosecond']
                duration = float(s*1000000000 + ns)/1000000000
                od['duration'] = "{}s".format(duration)
        
        v = find_key_value_in_dict(f, 'table_id')
        if (v != None and type(v) is int):
            od['table'] = v
        
        # Flow Statistics
        v = find_key_value_in_dict(f, 'packet-count')
        if (v != None and type(v) is int):
            od['n_packets'] = v

        v = find_key_value_in_dict(f, 'byte-count')
        if (v != None and type(v) is int):
            od['n_bytes'] = v

        v = find_key_value_in_dict(f, 'priority')
        if (v != None and type(v) is int):
            od['priority'] = v
            
        # Flow Match
        v = find_key_value_in_dict(f, 'match')
        if (v != None and type(v) is dict):            
            p = find_key_value_in_dict(v, 'in-port')
            if (p != None and isinstance(p, basestring)):
                od['in_port'] = string.replace(p, self.name + ":", '')
            
            vlanmatch = find_key_value_in_dict(v, 'vlan-match')
            if (vlanmatch != None and type(vlanmatch) is dict):
                if ('vlan-id' in vlanmatch and type(vlanmatch['vlan-id'] is dict)):
                    if ('vlan-id' in vlanmatch['vlan-id'] and type(vlanmatch['vlan-id']['vlan-id']) is int):
                        od['dl_vlan'] = vlanmatch['vlan-id']['vlan-id']
                
                if ('vlan-pcp' in vlanmatch and type(vlanmatch['vlan-pcp'] is int)):
                    od['dl_vlan_pcp'] = vlanmatch['vlan-pcp']
            
            ethermatch = find_key_value_in_dict(v, 'ethernet-match')
            if (ethermatch != None and type(v) is dict):
                ethertype = find_key_value_in_dict(ethermatch, 'type')
                if(ethertype != None and type(ethertype) is int):
                    od['dl_type'] = hex(ethertype)
                
                ethersrc = find_key_value_in_dict(ethermatch, 'ethernet-source')
                if(ethersrc != None and type(ethersrc) is dict):
                    addr = find_key_value_in_dict(ethersrc, 'address')
                    if(addr != None):
                        od['dl_src'] = addr
                
                etherdst = find_key_value_in_dict(ethermatch, 'ethernet-destination')
                if(etherdst != None and type(etherdst) is dict):
                    addr = find_key_value_in_dict(etherdst, 'address')
                    if(addr != None):
                        od['dl_dst'] = addr
            
            ipmatch = find_key_value_in_dict(v, 'ip-match')
            if (ipmatch != None and type(ipmatch) is dict):
                if('ip-protocol' in ipmatch and type(ipmatch['ip-protocol']) is int):                    
                    od['nw_proto'] = ipmatch['ip-protocol']
            
            tcpsrcport = find_key_value_in_dict(v, 'tcp-source-port')
            if (tcpsrcport != None and type(tcpsrcport) is int):
                od['tp_src'] = tcpsrcport
            
            ipv4src = find_key_value_in_dict(v, 'ipv4-source')
            if (ipv4src != None and isinstance(ipv4src, basestring)):
                od['nw_src'] = ipv4src
            
            ipv4dst = find_key_value_in_dict(v, 'ipv4-destination')
            if (ipv4dst != None and isinstance(ipv4dst, basestring)):
                od['nw_dst'] = ipv4dst
        
        # Flow Actions
        v = find_key_value_in_dict(f, 'instructions')
        if (v != None and type(v) is dict):
            v = find_key_value_in_dict(v, 'instruction')
            if (v != None and type(v) is list):
                if (len(v) != 0 and type(v[0]) is dict):
                    v = find_key_value_in_dict(v[0], 'apply-actions')
                    if (v != None and type(v) is dict):
                        v = find_key_value_in_dict(v, 'action')
                        if (v != None and type(v) is list):
                            astr = ""
                            al = self.__build_ovs_action_list(v)
                            if(al != None):
                                al.sort(key=self.__getOrderKey)
                                l = len(al)
                                i = 0
                                for a in al:
                                    astr += a.to_string()
                                    i += 1
                                    if(i < l):
                                        astr += ","

                            od['actions'] = '{}'.format(astr)
        # Following 'else' case is a hack, ODL flows do not seem to contain
        # the 'instructions' info for flows that were set with 'drop' action
        # TBD: Perhaps this hack should be removed!!!
        else:
            od['actions'] = 'drop'
                                    
#        print json.dumps(od, indent=4)
#        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        return od


    def __build_ovs_action_list(self, alist):
        al = []
        
        for item in alist:
            if ('output-action' in item):
                a = ActionOutput()
                a.update_from_list(item)
                al.append(a)

        return al

    def __getOrderKey(self, item):
        return item.order

    def __getPriorityKey(self, item):
        return item['priority']
    
    '''
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_connector_info(self):        
        status = OperStatus()
        info = {}
        ctrl = self.ctrl
        myname = self.name
        url = ctrl.get_node_operational_url(myname)
        
        resp = ctrl.http_get_request(url, data=None, headers=None)
        if(resp == None):
            status.set_status(STATUS.CONN_ERROR)
        elif(resp.content == None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        elif (resp.status_code == 200):
            dictionary = json.loads(resp.content)
            p2 = 'node-connector'
            vlist = find_key_values_in_dict(dictionary, p2)
            if (len(vlist) != 0 and (type(vlist[0]) is list)):
#                p3 = 'flow-node-inventory:flow-feature-capability-'
#                info = replace_str_in_dict(vlist[0], p3, '')
                print "+++++++++++++++"
#                print vlist[0]
#                print json.dumps(vlist[0], indent=4)
                print vlist[0]
                for item in vlist[0]:
#                    print type(item)
#                    print item
#                    print ",,,",
                    print ("   number: %s " % item['flow-node-inventory:port-number'])
                    print ("   name: %s " % item['flow-node-inventory:name'])
                    print ("   hardware address: %s " % item['flow-node-inventory:hardware-address'])
                    print ("   current feature: %s " % item['flow-node-inventory:current-feature'])
                    print ("------------------------------------------")
#                    print item['stp-status-aware-node-connector:status']
                    
#                    if type(item) is dict:
#                        print ",,,",
#                        print item
#                    print type(item)
                    
                status.set_status(STATUS.OK)
            else:
                print "---------------"
                status.set_status(STATUS.DATA_NOT_FOUND)
        else:
            status.set_status(STATUS.HTTP_ERROR, resp)
        
        return (status, info)                        
    '''

class ActionOutput():
    def __init__(self, port=None, length=None, order=None):        
        self.type = 'output'
        self.order = order
        self.action = {'port': port, 'max-len': length}
                
    def update(self, port=None, length=None, order=None):
        self.action = {'port': port, 'max-len': length}
        if(port != None):
            self.action['port'] = port
        if(length != None):
            self.action['max-len'] = length
        if(order != None):
            self.order = order
    
    def update_from_list(self, data):
        if(data != None and type(data) is dict and ('output-action' in data)):
            self.type = 'output'
            self.order = find_key_value_in_dict(data, 'order')
            self.action = {'port': None, 'max-len': None}
            self.action['port'] = find_key_value_in_dict(data, 'output-node-connector')
            self.action['max-len'] = find_key_value_in_dict(data, 'max-length')

    def to_string(self):
        s = ""
        p = self.action['port']
        l = self.action['max-len']
        if(p != None and l != None):
            if(p == 'CONTROLLER'):
                s = '{}:{}'.format(p, l)
            else:
                s = '{}:{}'.format(self.type, p)
        
        return s
