
# Copyright (c) 2015,  BROCADE COMMUNICATIONS SYSTEMS, INC

# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

"""

@authors: Sergei Garbuzov
@status: Development
@version: 1.1.0

notification.py: Parser for notification events received from Controller


"""

import os
import re
import xmltodict
from framework.common.utils import dbg_print

yang_namespace_to_prefix_map = {
    'urn:opendaylight:inventory' : 'inv',
    'urn:opendaylight:netconf-node-inventory' : 'netinv"',
    'urn:opendaylight:flow:inventory' : 'flownode',
    'urn:opendaylight:flow:statistics' : 'fstat',
    'urn:opendaylight:flow:table:statistics' : 'flowstat',
    'urn:opendaylight:port:statistics' : 'portstat',
    'urn:TBD:params:xml:ns:yang:network-topology' : 'nt',
    'urn:opendaylight:model:topology:inventory' : 'nt1',
    'urn:opendaylight:host-tracker' : 'host-track',
}

def yang_nsname_to_prefix(nsname):
    if nsname in yang_namespace_to_prefix_map:
        return yang_namespace_to_prefix_map[nsname]
    else:
        return nsname

def yang_prefix_to_nsname(prefix):
    for k, v in yang_namespace_to_prefix_map:
        if v == prefix:
            return k
    
    return prefix

#-------------------------------------------------------------------------------
# Class 'NetworkTopologyChangeNotification'
#-------------------------------------------------------------------------------
class NetworkTopologyChangeNotification():
    """ Parser for notification messages generated by the Controller
        when it detects changes in the network topology data tree """
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, event):
        self.added_switches = []
        self.removed_switches = []
        self.added_hosts = []
        self.removed_hosts = []
        self.added_links = []
        self.removed_links = []
        
        d = xmltodict.parse(event)
        try:
            p1 = 'notification'
            notification = d[p1]
            
            p2 = 'eventTime'
            self.timestamp = notification[p2]
            
            self.events = []
            p3 = 'data-changed-notification'
            p4 = 'data-change-event'
            events = notification[p3][p4]
            if isinstance(events, list):
                for item in events:
                    tc_evt = TopoChangeEvent(item)
                    self.events.append(tc_evt)
            elif isinstance(events, dict):
                tc_evt = TopoChangeEvent(events)
                self.events.append(tc_evt)
            else:
                msg = "DEBUG: events=%s, " \
                      "unexpected data format '%s'" % (events, type(events))
                dbg_print(msg)
            
            for event in self.events:
                if event.created():
                    if event.is_switch():
                        self.added_switches.append(event.get_node_id())
                    elif event.is_host():
                        self.added_hosts.append(event.get_node_id())
                    elif event.is_link():
                        self.added_links.append(event.get_link_id())
                elif event.deleted():
                    if event.is_switch():
                        self.removed_switches.append(event.get_node_id())
                    elif event.is_host():
                        self.removed_hosts.append(event.get_node_id())
                    elif event.is_link():
                        self.removed_links.append(event.get_link_id())
        except(Exception):
            msg = "DEBUG: failed to process event '%s'" % event
            dbg_print(msg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_time(self):
        return self.timestamp
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def switches_added(self):
        return self.added_switches
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def switches_removed(self):
        return self.removed_switches
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def hosts_added(self):
        return self.added_hosts 
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def hosts_removed(self):
        return self.removed_hosts
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def links_added(self):
        return self.added_links
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def links_removed(self):
        return self.removed_links
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def print_events(self):
        for event in self.events:
            if event.is_link():
                print "\n".strip()
                event.do_print()
                print "\n".strip()
            else:
                print "\n".strip()
                event.do_print()
                print "\n".strip()
    
#-------------------------------------------------------------------------------
# Class 'TopoChangeEvent'
#-------------------------------------------------------------------------------
class TopoChangeEvent():
    """ Parser for the data change event located in the network topology change
        notification message received from the Controller.
        Helper subclass for the 'NetworkTopologyChangeNotification' class """
      
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, event):
        p = 'path'
        if isinstance(event, dict):
            for k,v in event.items():
                if k == p:
                    self.path_info = PathInfo(v)
                else:
                    setattr(self, k, v)
        else:
            msg = "DEBUG: event=%s, " \
                  "unexpected data format '%s'" % (event, type(event))
            dbg_print(msg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def created(self):
        res = False
        p = 'operation'
        if hasattr(self, p):
            attr = getattr(self, p)
            res = (attr == 'created')
            
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def deleted(self):
        res = False
        p = 'operation'
        if hasattr(self, p):
            attr = getattr(self, p)
            res = (attr == 'deleted')
            
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def updated(self):
        res = False
        p = 'operation'
        if hasattr(self, p):
            attr = getattr(self, p)
            res = (attr == 'updated')
            
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_path(self):
        path = None
        p = 'path_info'
        if hasattr(self, p):
            path = str(self.path_info.path)
        
        return path
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def is_node(self):
        res = False
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            basename = os.path.basename(path)
            if basename:
                p1 = '.*node-id$'
                r = re.search(p1, basename)
                if r != None:
                    res = True
        
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def is_switch(self):
        res = False
        if self.is_node():
            node_id = self.get_node_id()
            if node_id and node_id.startswith('openflow'):
                res = True
        
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def is_host(self):
        res = False
        if self.is_node():
            node_id = self.get_node_id()
            if node_id and node_id.startswith('host'):
                res = True
        
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_node_id(self):
        node_id = None
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            chunks = repr(path).split(']')
            if chunks:
                p = 'node-id='
                for s in chunks:
                    idx = s.find(p)
                    if(idx >= 0):
                        node_id = s[idx + len(p):].translate(None , "[]'\"")
                        break
            
        return node_id
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def is_link(self):
        res = False
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            basename = os.path.basename(path)
            if basename:
                p1 = '.*link-id$'
                r = re.search(p1, basename)
                if r != None:
                    res = True
        
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_link_id(self):
        link_id = None
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            chunks = repr(path).split(']')
            if chunks:
                p = 'link-id='
                for s in chunks:
                    idx = s.find(p)
                    if(idx >= 0):
                        link_id = s[idx + len(p):].translate(None , "[]'\"")
                        break
        
        return link_id
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def do_print(self):
        print " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        print " operation: %s" % self.operation
        self.path_info.do_print()
        print " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

#-------------------------------------------------------------------------------
# Class 'InventoryChangeNotification'
#-------------------------------------------------------------------------------
class InventoryChangeNotification():
    """ Parser for notification messages generated by the Controller
        when it detects changes in its internal inventory data store """
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, event):
        self.added_nodes = []
        self.removed_nodes = []
        self.added_flows = []
        self.removed_flows = []
        
        d = xmltodict.parse(event)
        try:
            p1 = 'notification'
            notification = d[p1]
            
            p2 = 'eventTime'
            self.timestamp = notification[p2]
            
            self.events = []
            p3 = 'data-changed-notification'
            p4 = 'data-change-event'
            events = notification[p3][p4]
            if isinstance(events, list):
                for item in events:
                    evt = InventoryChangeEvent(item)
                    self.events.append(evt)
            elif isinstance(events, dict):
                evt = InventoryChangeEvent(events)
                self.events.append(evt)
            else:
                msg = "DEBUG: events=%s, " \
                      "unexpected data format '%s'" % (events, type(events))
                dbg_print(msg)
             
            for event in self.events:
                if event.created():
                    if event.is_node():
                        self.added_nodes.append(event.get_node_id())
                    elif event.is_flow_entry():
                        flow_info = FlowInfo(event)
                        self.added_flows.append(flow_info)
                elif event.deleted():
                    if event.is_node():
                        self.removed_nodes.append(event.get_node_id())
                    elif event.is_flow_entry():
                        flow_info = FlowInfo(event)
                        self.removed_flows.append(flow_info)
        except(Exception) as e:
            print "Error, %s" % e
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_time(self):
        return self.timestamp
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def nodes_added(self):
        return self.added_nodes
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def nodes_removed(self):
        return self.removed_nodes
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def flows_added(self):
        return self.added_flows
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def flows_removed(self):
        return self.removed_flows
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def print_events(self):
        for event in self.events:
            if event.created():
                print "\n".strip()
                event.do_print()
                print "\n".strip()

#-------------------------------------------------------------------------------
# Class 'InventoryChangeEvent'
#-------------------------------------------------------------------------------
class InventoryChangeEvent():
    """ Parser for the data change event located in the inventory change
        notification message received from the Controller.
        Helper subclass for the 'InventoryChangeNotification' class """
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, event):
        self.path_info = None
        p = 'path'
        if isinstance(event, dict):
            for k,v in event.items():
                if k == p:
                    self.path_info = PathInfo(v)
                else:
                    setattr(self, k, v)
        else:
            msg = "DEBUG: events=%s, " \
                  "unexpected data format '%s'" % (event, type(event))
            dbg_print(msg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def created(self):
        res = False
        p = 'operation'
        if hasattr(self, p):
            attr = getattr(self, p)
            res = (attr == 'created')
            
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def deleted(self):
        res = False
        p = 'operation'
        if hasattr(self, p):
            attr = getattr(self, p)
            res = (attr == 'deleted')
            
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def updated(self):
        res = False
        p = 'operation'
        if hasattr(self, p):
            attr = getattr(self, p)
            res = (attr == 'updated')
            
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_path(self):
        path = None
        p = 'path_info'
        if hasattr(self, p):
            path = str(self.path_info.path)
        
        return path
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def is_node(self):
        res = False
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            basename = os.path.basename(path)
            if basename:
                p1 = 'node\[.*:id=.*\]'
                r = re.search(p1, basename)
                if r != None:
                    res = True
        
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def is_switch(self):
        res = False
        if self.is_node():
            node_id = self.get_node_id()
            if node_id and node_id.startswith('openflow'):
                res = True
        
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_node_id(self):
        node_id = None
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            chunks = str(path).split('[')
            p = ':id='
            for s in chunks:
                idx = s.find(p)
                if(idx >= 0):
                    node_id = s[idx + len(p):].translate(None , "[]'\"")
                    break
        
        return node_id
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def is_flow_entry(self):
        res = False
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            basename = os.path.basename(path)
            if basename:
                p1 = 'flow\[.*:id=.*\]'
                r = re.search(p1, basename)
                if r != None:
                    res = True
    
        return res
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_flow_entry_id(self):
        flow_id = None
        p = 'path_info'
        if hasattr(self, p):
            path = self.path_info.path
            chunks = str(path).split('[')
            p = ':id='
            for s in chunks:
                idx = s.find(p)
                if(idx >= 0):
                    flow_id = s[idx + len(p):].translate(None , "[]'\"")
        
        return flow_id
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def do_print(self):
        print " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        print " operation: %s" % self.operation
        self.path_info.do_print()
        print " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


class FlowInfo():
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, event):
        self.node_id = None
        self.table_id = None
        self.flow_id = None
        
        if isinstance(event, InventoryChangeEvent) and event.is_flow_entry():
            path = event.get_path()
            try:
                chunks = path.split('/')
                l = []
                p = ':id='
                for s in chunks:
                    idx = s.find(p)
                    if idx >= 0:
                        l.append(s[idx + len(p):].translate(None, "'[]"))
                
                self.node_id  = l[0]
                self.table_id = l[1]
                self.flow_id  = l[2]
            except(Exception):
                msg = "DEBUG: unexpected string format: %s" % path
                dbg_print(msg)
        else:
            msg = "wrong class usage"
            dbg_print(msg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_string(self):
        s = "{node='%s', table='%s', flowid='%s'}" % (self.node_id,
                                                      self.table_id,
                                                      self.flow_id)
        return s

#-------------------------------------------------------------------------------
# Class 'PathInfo'
#-------------------------------------------------------------------------------
class PathInfo():
    """ Represents the path to the node in the Controller's internal data tree
        where the change has been detected.
        Helper subclass for the 'NetworkTopologyChangeNotification' and 
       'InventoryChangeNotification' classes """
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, info):
        self.namespaces = None
        self.path = None
        if isinstance(info, dict):
            p1 = '#text'
            p2 = '@xmlns'
            try:
                path = info[p1]
                namespaces = []
                for k, v in info.items():
                    if k.startswith(p2):
                        pfx = yang_nsname_to_prefix(v)
                        d = {'ns': v, 'pfx': pfx}
                        namespaces.append(d)
                        nickname = k.split(':')[-1]
                        path = path.replace(nickname, pfx)
                
                self.namespaces = namespaces
                self.path = path
            except:
                msg = "DEBUG: failed to process info '%s'" % info
                dbg_print(msg)
        elif isinstance(info, basestring):
            self.path = info
        else:
            msg = "DEBUG: info=%s, " \
                  "unexpected data format '%s'" % (info, type(info))
            dbg_print(msg)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def do_print(self):
        for ns in self.namespaces:
            print " namespace: %s (prefix: %s)" % (ns['ns'], ns['pfx'])
        print " path: %s" % self.path


