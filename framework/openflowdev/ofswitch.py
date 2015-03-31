
import string
import json
#import collections

from collections import OrderedDict

from framework.controller.openflownode import OpenflowNode
from framework.common.status import OperStatus, STATUS
from framework.common.utils import find_key_values_in_dict
from framework.common.utils import replace_str_value_in_dict
from framework.common.utils import find_key_value_in_dict
from framework.common.utils import find_dict_in_list
from framework.common.utils import remove_empty_from_dict


    
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class OFSwitch(OpenflowNode):
    """Class that represents an instance of 'OpenFlow Switch' (OpenFlow capable device)."""
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, ctrl=None, name=None, dpid=None):
        """Initializes this object properties."""
        super(OFSwitch, self).__init__(ctrl, name)
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
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
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
        
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_flows(self, tableid, operational=True):
        status = OperStatus()
        flows = {}
        url = ""
        templateUrlExt = "/flow-node-inventory:table/{}"
        urlext = templateUrlExt.format(tableid)
        ctrl = self.ctrl
        if (operational):
            url = ctrl.get_node_operational_url(self.name)
        else:
            url = ctrl.get_node_config_url(self.name)        
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
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_operational_flows(self, tableid):
        flows = {}
        result = self.get_flows(tableid, operational=True)
        status = result[0]
        if(status.eq(STATUS.OK) == True):
            flows = result[1]
        
        return (status, flows)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_operational_flows_ovs_syntax(self, tableid, sort=None):
        ovsflows = []
        result = self.get_operational_flows(tableid)
        status = result[0]
        if(status.eq(STATUS.OK) == True):
            flist = result[1]
            if (sort == True):
                flist.sort(key=self.__getPriorityKey)                
            for item in flist:
                f = self.odl_to_ovs_flow_syntax(item)
                ovsflows.append(f)

        return (status, ovsflows)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_configured_flows(self, tableid):
        flows = {}
        result = self.get_flows(tableid, operational=False)
        status = result[0]
        if(status.eq(STATUS.OK) == True):
            flows = result[1]
        
        return (status, flows)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_configured_flows_ovs_syntax(self, tableid, sort=None):
        ovsflows = []
        result = self.get_configured_flows(tableid)
        status = result[0]
        if(status.eq(STATUS.OK) == True):
            flist = result[1]
            if (sort == True):
                flist.sort(key=self.__getPriorityKey)                
            for item in flist:
                f = self.odl_to_ovs_flow_syntax(item)
                ovsflows.append(f)

        return (status, ovsflows)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def odl_to_ovs_flow_syntax(self, odlflow):
        od = OrderedDict()
#        print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
#        print (odlflow)
        
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

        v = find_key_value_in_dict(f, 'idle-timeout')
        if (v != None and type(v) is int and v != 0):
            od['idle_timeout'] = v

        v = find_key_value_in_dict(f, 'hard-timeout')
        if (v != None and type(v) is int and v != 0):
            od['hard_timeout'] = v
        
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
                    if(addr != None and isinstance(addr, basestring)):
                        od['dl_src'] = addr.lower()
                
                etherdst = find_key_value_in_dict(ethermatch, 'ethernet-destination')
                if(etherdst != None and type(etherdst) is dict):
                    addr = find_key_value_in_dict(etherdst, 'address')
                    if(addr != None and isinstance(addr, basestring)):
                        od['dl_dst'] = addr.lower()
            
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
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __build_ovs_action_list(self, alist):
        al = []
        
        for item in alist:
            if ('output-action' in item):
                a = ActionOutput()
                a.update_from_list(item)
                al.append(a)

        return al
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __getOrderKey(self, item):
        return item.order
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
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

#---------------------------------------------------------------------------
# 
#---------------------------------------------------------------------------
class ActionOutput():

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, port=None, length=None, order=None):        
        self.type = 'output'
        self.order = order
        self.action = {'port': port, 'max-len': length}
                
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def update(self, port=None, length=None, order=None):
        self.action = {'port': port, 'max-len': length}
        if(port != None):
            self.action['port'] = port
        if(length != None):
            self.action['max-len'] = length
        if(order != None):
            self.order = order
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def update_from_list(self, data):
        if(data != None and type(data) is dict and ('output-action' in data)):
            self.type = 'output'
            self.order = find_key_value_in_dict(data, 'order')
            self.action = {'port': None, 'max-len': None}
            self.action['port'] = find_key_value_in_dict(data, 'output-node-connector')
            self.action['max-len'] = find_key_value_in_dict(data, 'max-length')

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class FlowEntry(object):
    ''' Class for creating and interacting with OpenFlow flows '''
    _mn = "flow-node-inventory:flow"

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        ''' Opaque Controller-issued identifier '''
        self.cookie = 0
        
        ''' Mask used to restrict the cookie bits that must match when the command is
            OFPFC_MODIFY* or OFPFC_DELETE*. A value of 0 indicates no restriction '''
        self.cookie_mask = 0  
          
        ''' ID of the table to put the flow in '''
        self.table_id = ""
        
        ''' Priority level of flow entry '''
        self.priority = 0
        
        ''' Idle time before discarding (seconds) '''
        self.idle_timeout = 0
        
        ''' Max time before discarding (seconds) '''
        self.hard_timeout = 0 
           
        ''' Modify/Delete entry strictly matching wildcards and priority '''
#        self.strict = "false"
        self.strict = False
        
        ''' For OFPFC_DELETE* commands, require matching entries to include this as an
            output port. A value of OFPP_ANY indicates no restriction. '''
        self.out_port = ""
        
        ''' For OFPFC_DELETE* commands, require matching entries to include this as an
            output group. A value of OFPG_ANY indicates no restriction '''
        self.out_group = ""
        
        ''' Bitmap of OFPFF_* flags '''
        self.flags = ""
        
        ''' This FlowEntry name in the FlowTable (internal Controller's inventory attribute) '''
        self.flow_name = ""
        
        ''' This FlowEntry identifier in the FlowTable (internal Controller's inventory attribute) '''    
        self.id = ""
        
        ''' ??? (internal Controller's inventory attribute) '''
        self.installHw = False
        
        ''' Boolean flag used to enforce OpenFlow switch to do ordered message processing.
            Barrier request/reply messages are used by the controller to ensure message dependencies
            have been met or to receive notifications for completed operations. When the controller
            wants to ensure message dependencies have been met or wants to receive notifications for
            completed operations, it may use an OFPT_BARRIER_REQUEST message. This message has no body.
            Upon receipt, the switch must finish processing all previously-received messages, including
            sending corresponding reply or error messages, before executing any messages beyond the
            Barrier Request. '''
        self.barrier=False
        
        ''' Buffered packet to apply to, or OFP_NO_BUFFER. Not meaningful for OFPFC_DELETE* '''
        self.buffer_id = ""
        
        '''  Flow match fields '''
        self.match = {}

        ''' Instructions to be executed when a flow matches this entry flow match fields '''
        self.instructions = {}
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        """ Return FlowEntry as JSON """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_payload(self):
        s = self.to_json()
        s = string.replace(s, 'idle_timeout', 'idle-timeout')
        s = string.replace(s, 'hard_timeout', "hard-timeout")
        s = string.replace(s, 'apply_actions', "apply-actions")
        s = string.replace(s, 'drop_action', "drop-action")
        s = string.replace(s, 'output_action', "output-action")
        d1 = json.loads(s)
        d2 = remove_empty_from_dict(d1)
        payload = {self._mn : d2}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_instruction(self, instruction):
        self.instructions.update({'instruction':instruction})

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_match(self, match):
        print type(match)
        self.match.update(match.__dict__)
#        self.match.update(match)
        '''
        key = match.get_key()
        if (key != None):
            self.match.update({key:match})
        else:
            self.match.update({match})
        '''

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Instructions():
    """The class that defines OpenFlow flow Instructions""" 
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.instructions = {}

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_instruction(self, instruction):
        self.instructions.append(instruction)

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Instruction():
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, order=0):
        self.order = order
        self.apply_actions = {}

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_action(self, action):
        self.actions.append(action)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def add_apply_action(self, action):
        self.apply_actions.update({'action':action})

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Action(object):
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, order=None):
        self.order = order

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class DropAction(Action):
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, order=None):
        super(DropAction, self).__init__(order)
        self.drop_action = {}

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_order(self, order):
        self.order = order
    
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class OutputAction(Action):
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, order=0, port=0, max_len=0):
        super(OutputAction, self).__init__(order)
        self.output_action = {'output-node-connector' : port, 'max-length' : max_len }

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_outport(self, port):
        self.output_action['output-node-connector'] = port

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_max_len(self, max_len):
        self.output_action['max-length'] = max_len

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_order(self, order):
        self.order = order

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Match(object):
    """Class that represents OpenFlow flow matching attributes """
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        ''' Ingress port. Numerical representation of in-coming port, starting at 1
            (may be a physical or switch-defined logical port) '''
        self.in_port = ""
        
        ''' Physical port (in 'ofp_packet_in messages', underlying physical port when
            packet received on a logical port) '''
        self.in_phy_port = ""
        
        ''' Ethernet match fields: 
            - ethernet destination MAC address
            - ethernet source MAC address
            - ethernet type of the OpenFlow packet payload (after VLAN tags) '''
        self.ethernet_match = EthernetMatch()
        
        ''' IPv4 source address (can use subnet mask) '''
        self.ipv4_source = ""
        
        ''' IPv4 destination address (can use subnet mask) '''
        self.ipv4_destination = ""
        
        ''' IP match fields:
            - Differentiated Service Code Point (DSCP). Part of the IPv4 ToS field or
              the IPv6 Traffic Class field.
            - ECN bits of the IP header. Part of the IPv4 ToS field or
              the IPv6 Traffic Class field 
            - IPv4 or IPv6 protocol number '''
        self.ip_match = IpMatch()
        
        ''' IPv6 source address (can use subnet mask) '''
        self.ipv6_source = ""
        
        ''' IPv6 destination address (can use subnet mask) '''
        self.ipv6_destination = ""
        
        ''' The target address in an IPv6 Neighbor Discovery message '''
        self.ipv6_nd_target = ""
        
        ''' The source link-layer address option in an IPv6 Neighbor Discovery message '''
        self.ipv6_nd_sll = ""
        
        ''' The target link-layer address option in an IPv6 Neighbor Discovery message '''
        self.ipv6_nd_tll = ""
        
        ''' IPv6 flow label '''
        self.ipv6_label = Ipv6Label()
        
        ''' IPv6 Extension Header pseudo-field '''
        self.ipv6_ext_header = Ipv6ExtHdr()
        
        ''' Protocol match fields:
           - The LABEL in the first MPLS shim header
           - The TC in the first MPLS shim header
           - The BoS bit (Bottom of Stack bit) in the first MPLS shim header
           - The I-SID in the first PBB service instance tag '''
        self.protocol_match_fields = ProtocolMatchFields()
        
        ''' UDP source port '''
        self.udp_source_port = ""
        
        ''' UDP destination port '''
        self.udp_destination_port = ""
        
        ''' TCP source port '''
        self.tcp_source_port = ""
        
        ''' TCP destination port '''
        self.tcp_destination_port = ""
        
        ''' SCTP source port '''
        self.sctp_source_port = ""
        
        ''' SCTP destination port '''
        self.sctp_destination_port = ""
        
        ''' ICMP type '''
        self.icmpv4_type = ""
        
        ''' ICMP code'''
        self.icmpv4_code = ""
        
        ''' ICMPv6 type '''
        self.icmpv6_type = ""
        
        ''' ICMPv6 code '''
        self.icmpv6_code = ""        
        
        ''' VLAN match fields:
            - VLAN-ID from 802.1Q header (the CFI bit indicate the presence of a valid VLAN-ID)
            - VLAN-PCP from 802.1Q header
        '''
        self.vlan_match = VlanMatch()
                
        ''' ARP opcode '''
        self.arp_op = ""
        
        ''' Source IPv4 address in the ARP payload (can use subnet mask) '''
        self.arp_source_transport_address = ""
        
        ''' Target IPv4 address in the ARP payload (can use subnet mask) '''
        self.arp_target_transport_address = ""
        
        ''' Source Ethernet address in the ARP payload '''
        self.arp_source_hardware_address = ArpSrcHwAddrMatch()
        
        ''' Target Ethernet address in the ARP payload '''
        self.arp_target_hardware_address = ArpTgtHwAddrMatch()
        
        ''' Metadata associated with a logical port '''
        self.tunnel = Tunnel()

        ''' Table metadata (used to pass information between tables) '''
        self.metadata = Metadata()
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_eth_type(self, eth_type):
        self.ethernet_match.ethernet_type = eth_type
#        self.ethernet_match.set_type(eth_type)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_eth_src(self, eth_src):
        self.ethernet_match.ethernet_source = eth_src
#        self.ethernet_match.set_src(eth_src)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_eth_dst(self, eth_dst):
        self.ethernet_match.ethernet_destination = eth_dst        
#        self.ethernet_match.set_dst(eth_dst)

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ipv4_src(self, ipv4_src):
        self.ipv4_source = ipv4_src

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ipv4_dst(self, ipv4_dst):
        self.ipv4_destination = ipv4_dst

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ipv6_src(self, ipv6_src):
        self.ipv6_source = ipv6_src

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ipv6_dst(self, ipv6_dst):
        self.ipv6_destination = ipv6_dst    
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ip_dscp(self, ip_dscp):
        self.ip_match.ip_dscp = ip_dscp

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ip_ecn(self, ip_ecn):
        self.ip_match.ip_ecn = ip_ecn

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ip_proto(self, ip_proto):
        self.ip_match.ip_protocol = ip_proto

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    '''        
    def ip_proto_version(self, version):
        self.ip_match.ip_proto = version    
    '''    

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_udp_src(self, udp_port):
        self.udp_source_port = udp_port

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_udp_dst(self, udp_port):
        self.udp_destination_port = udp_port

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_tcp_src(self, tcp_port):
        self.tcp_source_port = tcp_port

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_tcp_dst(self, tcp_port):
        self.tcp_destination_port = tcp_port        

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_sctp_src(self, sctp_port):
        self.sctp_source_port = sctp_port

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def sctp_dst(self, sctp_port):
        self.sctp_destination_port = sctp_port
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_icmpv4_type(self, icmpv4_type):
        self.icmpv4_type = icmpv4_type

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_icmpv4_code(self, icmpv4_code):
        self.icmpv4_code = icmpv4_code        
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_icmpv6_type(self, icmpv6_type):
        self.icmpv6_type = icmpv6_type
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_icmpv6_code(self, icmpv6_code):
        self.icmpv6_code = icmpv6_code        
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_in_port(self, in_port):
        self.in_port = in_port
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_in_phy_port(self, in_phy_port):
        self.in_phy_port = in_phy_port
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_arp_opcode(self, arp_opcode):
        self.arp_op = arp_opcode
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_arp_src_transport_address(self, ip_addr):
        self.arp_source_transport_address = ip_addr        
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_arp_tgt_transport_address(self, ip_addr):
        self.arp_target_transport_address = ip_addr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_arp_src_hw_address(self, mac_addr):
        self.arp_source_hardware_address.address = mac_addr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_arp_tgt_hw_address(self, mac_addr):
        self.arp_target_hardware_address = mac_addr    
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_tunnel_id(self, tunnel_id):
        self.tunnel.tunnel_id = tunnel_id
    
#    def __getattr__(self, attr):
#         return self[attr]
        
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class EthernetMatch(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.ethernet_type = ""
        self.ethernet_source = ""
        self.ethernet_destination = ""
    
    '''
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ether_type(self, ether_type):
        self.ethernet_type = ether_type
    '''
    '''
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_key(self):
        return "ethernet-match"
    '''
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class VlanMatch(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        ''' VLAN-ID from 802.1Q header '''
        self.vlan_id = VlanId()
        
        ''' VLAN-PCP from 802.1Q header '''
        self.vlan_pcp = ""
    
    '''
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_vid(self, vid):
        self.vlan_id = vid
        self.vlan_id_present = True
    '''
    
    '''
    def get_key(self):
        return "vlan-match"
    '''

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class VlanId(VlanMatch):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        ''' VLAN-ID from 802.1Q header '''
        self.vlan_id = ""
        
        ''' Flag that indicates that 'vlan_id' value is set and matching is
            only for packets with VID equal to 'vlan_id' value '''
        self.vlan_id_present = False

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class IpMatch(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
#        self.ip_protocol = ""
        ''' "IP DSCP (6 bits in ToS field) '''
        self.ip_dscp = ""
        
        ''' IP ECN (2 bits in ToS field) '''
        self.ip_ecn = ""
        
        ''' IP protocol (IPv4 or IPv6 Protocol Number)'''
        self.ip_proto = ""
    '''
    def get_key(self):
        return "ip-match"
    pass
    '''

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Ipv6Label(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.ipv6_flabel = ""
        self.flabel_mask = ""

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Ipv6ExtHdr(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.ipv6_exthdr = ""
'''
class Ipv4Match(Match):
    def __init__(self):
        self.ipv4_source = ""
        self.ipv4_destination = ""
    def get_key(self):
        return None
'''

'''
class Ipv6Match(Match):
    pass
'''

'''
class UdpMatch(Match):
    pass
'''

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class ProtocolMatchFields(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        ''' The LABEL in the first MPLS shim header '''
        self.mpls_label = ""
        
        ''' The TC in the first MPLS shim header '''
        self.mpls_tc = ""
        
        ''' The BoS bit (Bottom of Stack bit) in the first MPLS shim header '''
        self.mpls_bos = ""
        
        ''' The I-SID in the first PBB service instance tag '''
        self.pbb = Pbb()

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Pbb(ProtocolMatchFields):
    ''' The I-SID in the first PBB service instance tag '''
     
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.pbb_isid = ""
        self.pbb_mask = ""
        
    '''
    def get_key(self):
        return "protocol-match-fields"
    pass
    '''

'''
class TcpMatch(Match):
    def __init__(self):
        self.tcp_source_port = ""
        self.tcp_destination_port = ""
    def get_key(self):
        return None
'''

'''
class SctpMatch(Match):
    pass
'''

'''
class Icmpv4Match(Match):
    pass
'''

'''
class Icmpv6Match(Match):
    pass
'''

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class ArpSrcHwAddrMatch(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.address = ""

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class ArpTgtHwAddrMatch(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.address = ""

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Tunnel(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        ''' Metadata associated with a logical port'''
        self.tunnel_id = ""

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Metadata(Match):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.metadata = ""
        self.metadata_mask = ""
'''
class TcpFlagMatch(Match):
    pass
'''

'''
class TunnelIpv4Match(Match):
    pass
'''

''' Tmp code - START '''
if __name__ == "__main__":
    print "Start"
    flow = FlowEntry()
    
    instruction_order = "1"
    instruction = Instruction(instruction_order)

    action_order = "1"
    action = DropAction(action_order)
    
    instruction.add_apply_action(action)
    
    flow.add_instruction(instruction)

    
    match = Match()
    
    eth_type = 34525
    match.set_eth_type(eth_type)
    
    eth_src = "00:00:00:11:23:ae"
    match.set_eth_src(eth_src)
    
    eth_dst = "ff:ff:29:01:19:61"
    match.set_eth_dst(eth_dst)
    
    ipv4_src = "17.1.2.3/8"
    match.set_ipv4_src(ipv4_src)
    
    ipv4_dst = "172.168.5.6/16"
    match.set_ipv4_dst(ipv4_dst)
    
    ipv6_src = "fe80::2acf:e9ff:fe21:6431/128"
    match.set_ipv6_src(ipv6_src)
    
    ipv6_dst = "aabb:1234:2acf:e9ff::fe21:6431/64"
    match.set_ipv6_dst(ipv6_dst)
    
    ip_dscp = 2
    match.set_ip_dscp(ip_dscp)
    
    ip_ecn = 2
    match.set_ip_ecn(ip_ecn)
    
    ip_proto = 6
    match.set_ip_proto(ip_proto)
    
    tcp_src = 25364
    match.set_tcp_src(tcp_src)
    
    tcp_dst = 8080
    match.set_tcp_dst(tcp_dst)
    
    icmpv4_type = 6
    match.set_icmpv4_type(icmpv4_type)
    
    icmpv4_code = 3
    match.set_icmpv4_code(icmpv4_code)
    
    tunnel_id = 2591
    match.set_tunnel_id(tunnel_id)
    
    in_port = 1
    match.set_in_port(in_port)
    
    in_phy_port = 2
    match.set_in_phy_port(in_phy_port)
    
    flow.add_match(match)
    '''
    ether_match = EthernetMatch()
    etype = 34525
    ether_match.set_ether_type(etype)
    
    flow.add_match(ether_match)
    '''





    flow_json = flow.to_json()
    print "flow JSON"
    print flow_json
    
    '''
    flow_payload = flow.get_payload()
    print "flow HTTP payload"
    print flow_payload
    '''
 
    #------------------------------------------
    '''
    flow = FlowEntry()

    instruction_order = "1"
    instruction = Instruction(instruction_order)

    action_order = "1"
    portnum = 3
    max_pkt_len = 60
    action = OutputAction(action_order, portnum, max_pkt_len)
    
    instruction.add_apply_action(action)
    
    flow.add_instruction(instruction)
    
    flow_json = flow.to_json()
    print "flow JSON"
    print flow_json
    
    flow_payload = flow.get_payload()
    print "flow HTTP payload"
    print flow_payload
    '''
    
''' Tmp code - END'''
    
'''
enum ofp_instruction_type {
OFPIT_GOTO_TABLE = 1,     /* Setup the next table in the lookup pipeline */
OFPIT_WRITE_METADATA = 2, /* Setup the metadata field for use later in pipeline */
OFPIT_WRITE_ACTIONS = 3,  /* Write the action(s) onto the datapath action set */
OFPIT_APPLY_ACTIONS = 4,  /* Applies the action(s) immediately */
OFPIT_CLEAR_ACTIONS = 5,  /* Clears all actions from the datapath action set */
OFPIT_METER = 6,          /* Apply meter (rate limiter) */
OFPIT_EXPERIMENTER = 0xFFFF /* Experimenter instruction */
};
'''
'''
enum ofp_action_type {
OFPAT_OUTPUT = 0,        /* Output to switch port. */
OFPAT_COPY_TTL_OUT = 11, /* Copy TTL "outwards" -- from next-to-outermost to outermost */
OFPAT_COPY_TTL_IN = 12,  /* Copy TTL "inwards" -- from outermost to next-to-outermost */
OFPAT_SET_MPLS_TTL = 15, /* MPLS TTL */
OFPAT_DEC_MPLS_TTL = 16, /* Decrement MPLS TTL */
OFPAT_PUSH_VLAN = 17,    /* Push a new VLAN tag */
OFPAT_POP_VLAN = 18,     /* Pop the outer VLAN tag */
OFPAT_PUSH_MPLS = 19,    /* Push a new MPLS tag */
OFPAT_POP_MPLS = 20,     /* Pop the outer MPLS tag */
OFPAT_SET_QUEUE = 21,    /* Set queue id when outputting to a port */
OFPAT_GROUP = 22,        /* Apply group. */
OFPAT_SET_NW_TTL = 23,   /* IP TTL. */
OFPAT_DEC_NW_TTL = 24,   /* Decrement IP TTL. */
OFPAT_SET_FIELD = 25,    /* Set a header field using OXM TLV format. */
OFPAT_PUSH_PBB = 26,     /* Push a new PBB service tag (I-TAG) */
OFPAT_POP_PBB = 27,      /* Pop the outer PBB service tag (I-TAG) */
OFPAT_EXPERIMENTER = 0xffff
};
'''
'''
5.9 Instructions
Each flow entry contains a set of instructions that are executed when a packet matches the entry. These
instructions result in changes to the packet, action set and/or pipeline processing.
A switch is not required to support all instruction types, just those marked
\Required Instruction" below. The controller can also query the switch about which of the
\Optional Instruction" types it supports.

Optional Instruction: Meter meter_id: Direct packet to the specified meter. As the result of
the metering, the packet may be dropped (depending on meter configuration and state).

Optional Instruction: Apply-Actions action(s): Applies the specific action(s) immediately,
without any change to the Action Set. This instruction may be used to modify the packet between
two tables or to execute multiple actions of the same type. The actions are specified as an action
list (see 5.11).

Optional Instruction: Clear-Actions: Clears all the actions in the action set immediately.

Required Instruction: Write-Actions action(s): Merges the specified action(s) into the current
action set (see 5.10). If an action of the given type exists in the current set, overwrite it, otherwise
add it.

Optional Instruction: Write-Metadata metadata / mask: Writes the masked metadata value
into the metadata field. The mask specifies which bits of the metadata register should be modified
(i.e. new metadata = old metadata & ~mask | value & mask).

Required Instruction: Goto-Table next-table-id: Indicates the next table in the processing
pipeline. The table-id must be greater than the current table-id. The flow entries of the last table
of the pipeline can not include this instruction (see 5.1). OpenFlow switches with only a single
flow table are not required to implement this instruction.

The instruction set associated with a flow entry contains a maximum of one instruction of each type. The
instructions of the set execute in the order specified by this above list. In practice, the only constraints
are that the Meter instruction is executed before the Apply-Actions instruction, that the Clear-Actions
instruction is executed before the Write-Actions instruction, and that Goto-Table is executed last.

A switch must reject a flow entry if it is unable to execute the instructions associated with the flow
entry. In this case, the switch must return an unsupported flow error (see 6.4). Flow tables may not
support every match, every instruction or every action.

5.10 Action Set
An action set is associated with each packet. This set is empty by default. A ow entry can modify the
action set using a Write-Action instruction or a Clear-Action instruction associated with a particular
match. The action set is carried between ow tables. When the instruction set of a ow entry does
not contain a Goto-Table instruction, pipeline processing stops and the actions in the action set of the
packet are executed.
An action set contains a maximum of one action of each type.

5.12 Actions
A switch is not required to support all action types, just those marked "Required Action" below. The
controller can also query the switch about which of the "Optional Action" it supports.

Required Action: Output. The Output action forwards a packet to a specified OpenFlow port (see4.1). 
OpenFlow switches must support forwarding to physical ports, switch-defined logical ports and
the required reserved ports (see 4.5).

Optional Action: Set-Queue. The set-queue action sets the queue id for a packet. When the packet is
forwarded to a port using the output action, the queue id determines which queue attached to this port
is used for scheduling and forwarding the packet. Forwarding behavior is dictated by the configuration
of the queue and is used to provide basic Quality-of-Service (QoS) support (see section 7.2.2).

Required Action: Drop. There is no explicit action to represent drops. Instead, packets whose action
sets have no output actions should be dropped. This result could come from empty instruction sets or
empty action buckets in the processing pipeline, or after executing a Clear-Actions instruction.

Required Action: Group. Process the packet through the specified group. The exact interpretation
depends on group type.

Optional Action: Push-Tag/Pop-Tag. Switches may support the ability to push/pop tags as shown in Table 6.
To aid integration with existing networks, we suggest that the ability to push/pop VLAN tags be supported.
Newly pushed tags should always be inserted as the outermost tag in the outermost valid location for
that tag. When a new VLAN tag is pushed, it should be the outermost tag inserted, immediately after
the Ethernet header and before other tags. Likewise, when a new MPLS tag is pushed, it should be the
outermost tag inserted, immediately after the Ethernet header and before other tags.
When multiple push actions are added to the action set of the packet, they apply to the packet in the
order defined by the action set rules, first MPLS, then PBB, than VLAN (see 5.10). When multiple push
actions are included in an action list, they apply to the packet in the list order (see 5.11)
'''
