#!/usr/bin/env python

"""
Copyright (c) 2015

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 - Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
-  Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
-  Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES;LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@authors: Sergei Garbuzov

"""

import yaml
import sys, argparse, logging

from framework.controller.controller import Controller
from framework.controller.inventory import Inventory
from framework.controller.topology import Topology, Node
from framework.controller.inventory import OpenFlowCapableNode

from framework.common.status import STATUS

#-------------------------------------------------------------------------------
# Class 'CtrlCfg'
#-------------------------------------------------------------------------------
class CtrlCfg():
    def __init__(self, addr, port, name, pswd):
        self.ip_addr    = addr
        self.tcp_port   = port
        self.admin_name = name
        self.admin_pswd = pswd
    
    def to_string(self):
        return "%s:%s" % (self.ip_addr, self.tcp_port)

#-------------------------------------------------------------------------------
# Class 'TopologyShow'
#-------------------------------------------------------------------------------
class TopologyInfo():
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self, ctrl):
        self.ctrl = ctrl
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def show_common(self, verbose=False):
        ctrl = self.ctrl
        result = ctrl.build_inventory_object()
        status = result.get_status()
        if(status.eq(STATUS.OK) == True):
            inventory = result.get_data()
            assert(isinstance(inventory, Inventory))
        else:
            print ("\n")
            print ("!!!Error, failed to obtain inventory info, reason: %s"
                   % status.brief().lower())
            exit(1)
        
        result = ctrl.get_topology_ids()
        status = result.get_status()
        if(status.eq(STATUS.OK) == True):
            topology_ids = result.get_data()
            assert(isinstance(topology_ids, list))
        else:
            print ("\n")
            print ("!!!Error, failed to obtain topology info, reason: %s"
                   % status.brief().lower())
            exit(1)

        topologies = []
        for topo_id in topology_ids:
            result = ctrl.build_topology_object(topo_id)
            status = result.get_status()
            if(status.eq(STATUS.OK) == True):
                topo  = result.get_data()
                topologies.append(topo)
                assert(isinstance(topo, Topology))
            else:
                print ("\n")
                print ("!!!Error, failed to parse '%s' topology info, reason: %s" 
                       % (topo_id, status.brief().lower()))
                exit(1)
        
        for topo in topologies:
            print "\n".strip()
            print (" Network topology '%s'") % topo.get_id()
            print "\n".strip()
            
            flows_cnt = 0
            sids =  topo.get_switch_ids()
            for sid in sids:
                flows_cnt += inventory.get_openflow_node_flows_cnt(sid)
            
            print ("   Number of flows              : %s" % flows_cnt)
            print ("   Number of switches           : %s" % topo.get_switches_cnt())
            print ("   Number of inter-switch links : %s" % topo.get_inter_switch_links_cnt())
            print ("   Number of hosts              : %s" % topo.get_hosts_cnt())
            
            if (verbose):
                print "\n".strip()
                print ("   Switches in topology")
                s1 = 'IP Address'
                s2 = 'OpenFlow Id'
                s3 = 'Flows Cnt'
                sym = '-'
                print "\n".strip()
                print "     {0:<15}  {1:<30}".format(s1, s2)
                print "     {0:<15}  {1:<30}".format(sym*15, sym*30)
                switch_ids =  topo.get_switch_ids()
                for switch_id in switch_ids:
                    inv_node = inventory.get_openflow_node(switch_id)
                    addr = inv_node.get_ip_address()
                    print "     {0:<15}  {1:<30}".format(addr, switch_id)
                
                print "\n".strip()
                print ("   Hosts in topology")
                s4 = 'IP Address'
                s5 = 'MAC Address'
                print "\n".strip()
                print "     {0:<15}  {1:<17}".format(s4, s5)
                print "     {0:<15}  {1:<17}".format(sym*15, sym*17)
                host_ids = topo.get_host_ids()
                for host_id in host_ids:
                    topo_node = topo.get_node_by_id(host_id)
                    mac = topo_node.get_mac_address()
                    ipaddr = topo_node.get_ip_address_for_mac(mac)
                    print "     {0:<15}  {1:<17}".format(ipaddr, mac)
                
                
                print "\n".strip()
                print ("   Flows per switch")
                print "\n".strip()
                print "     {0:<30}  {1:<10}".format(s2, s3)
                print "     {0:<30}  {1:<10}".format(sym*30, sym*10)
                for switch_id in switch_ids:
                    fcnt = inventory.get_openflow_node_flows_cnt(switch_id)
                    print "     {0:<30}  {1:<10}".format(switch_id, fcnt)
            
            print"\n"
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def show_switch(self, switch_id, verbose=False):
        ctrl = self.ctrl
        switch_inv = None
        switch_topo = None
        
        result = ctrl.build_openflow_node_inventory_object(switch_id)
        status = result.get_status()
        if(status.eq(STATUS.OK) == True):
            switch_inv = result.get_data()
            assert(isinstance(switch_inv, OpenFlowCapableNode))
        else:
            print ("\n")
            print ("!!!Error, failed to get inventory info for '%s' switch, reason: %s"
                   % (switch_id, status.brief().lower()))
            exit(1)
        
        topo_id = "flow:1"
        result = ctrl.build_topology_object(topo_id)
        status = result.get_status()
        if(status.eq(STATUS.OK) == True):
            topo = result.get_data()
            assert(isinstance(topo, Topology))
            switch_topo = topo.get_switch(switch_id)
            assert(isinstance(switch_topo, Node))
            assert(switch_topo.is_switch())
        else:
            print ("\n")
            print ("!!!Error, failed to parse '%s' topology info, reason: %s" 
                   % (topo_id, status.brief().lower()))
            exit(1)
        
        print "\n".strip()
        print " Switch '%s'" % switch_id
        print "\n".strip()
        print "   IP Address      : %s" % switch_inv.get_ip_address()
        print "   Max tables      : %s" % switch_inv.get_max_tables_info()
        print "   Number of flows : %s" % switch_inv.get_flows_cnt()
        clist = switch_inv.get_capabilities()
        g = 2
        chunks=[clist[x:x+g] for x in xrange(0, len(clist), g)]
        s = 'Capabilities'
        print "   %s    :" % s,
        for i in range(0, len(chunks)):
            n = 0 if i == 0 else len(s) + 9
            print "%s%s" % (" "*n, ", ".join(chunks[i]))
        
        print "\n".strip()
        
        s1 = "Port "
        s2 = "Name"
        s3 = "OpenFlow Id"
        sym = '-'
        print "   {0:<10}  {1:<16}  {2:<30}".format(s1, s2, s3)
        print "   {0:<10}  {1:<16}  {2:<30}".format(sym*10, sym*16, sym*30)
        pids = switch_inv.get_port_ids()
        for pid in pids:
            pnum = switch_inv.get_port_number(pid)
            pname =  switch_inv.get_port_name(pid)
            print "   {0:<10}  {1:<16}  {2:<30}".format(pnum, pname, pid)
            
        print "\n".strip()
        
        if (verbose):
            pnums = switch_topo.get_port_numbers()
            for pnum in pnums:
                if pnum == 'LOCAL':
                    continue
                print "   Port '%s' connected devices" % pnum
                print "\n".strip()
                plist = topo.get_peer_list_for_node_port_(switch_topo, pnum)
                for item in plist:
                    assert(isinstance(item, Node))
                    if(item.is_switch()):
                        print "     Device Type : %s" % "switch"
                        print "     OpenFlow Id : %s"  % item.get_openflow_id()
                    elif (item.is_host()):
                        print "     Device Type : %s" % "host"
                        mac_addr = item.get_mac_address()
                        print "     MAC Address : %s"  % mac_addr
                        ip_addr = item.get_ip_address_for_mac(mac_addr)
                        print "     IP Address  : %s"  % ip_addr
                    
                    print "\n".strip()

#-------------------------------------------------------------------------------
# Class 'OFToolParser'
#-------------------------------------------------------------------------------
class OFToolParser(object):
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.prog = 'oftool'
        parser = argparse.ArgumentParser(
            prog=self.prog,
            description='Command line tool for interaction with OpenFlow Controller',
            usage="%(prog)s [-h] [-C <path>] <command> [<args>]\n"
                     "\nAvailable commands are:\n"
                     "\n   show-topo       Show topology info"
                     "\n   show-inv        Show inventory info"
                     "\n   show-flow       Show flow(s)"
                     "\n   clear-flow      Delete flow(s)"
                     "\n"
                     "\n  'git help <command>' provides details for a specific command")
        parser.add_argument('-C', metavar="<path>",
                            dest='ctrl_cfg_file',
                            help="path to the controller's configuration file "
                                 "(default is './ctrl.yml')",
                            default="./ctrl.yml")
        parser.add_argument('command', help='command to be executed')
        args, remaining_args = parser.parse_known_args()

        # Get Controller's attributes from configuration file
        self.ctrl_cfg  = self.get_ctrl_cfg(args.ctrl_cfg_file)
        if(self.ctrl_cfg == None):
            print "\n".strip()
            print ("Error, failed to get Controller's configuration file %s" 
                   % args.ctrl_cfg_file)
            print "\n".strip()
            exit(1)
        
        # Invoke method that is matching the name of sub-command argument
        cmd = args.command.replace('-', '_')
        if hasattr(self, cmd):
            getattr(self, cmd)(remaining_args)
        else:
            print "\n".strip()
            print ("Error, unrecognized command '%s'" % cmd)
            print "\n".strip()
            parser.print_help()
            exit(1)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def show_topo(self, options):
        parser = argparse.ArgumentParser(
            prog=self.prog,
            description='Show topology information',
            usage="%(prog)s show-topo [-s=OPENFLOWID] [-v|--verbose]"
                  "\n\n"
                  "Show topology information currently known to the controller\n\n"
                  "  -s   provide information for a given switch\n"
                  "  -v   show detailed information\n")
        parser.add_argument("-v", '--verbose', action="store_true",
                            help="output details level")
        parser.add_argument('-s', '--switch', metavar = "SWITCHID")
        parser.add_argument('-U', action="store_true", dest="usage", help=argparse.SUPPRESS)
        args = parser.parse_args(options)
        if(args.usage):
            parser.print_usage()
            print "\n".strip()
            return
        
        print "\n".strip()
        print " [Controller '%s']" % self.ctrl_cfg.to_string()
        ctrl = Controller(self.ctrl_cfg.ip_addr, self.ctrl_cfg.tcp_port,
                          self.ctrl_cfg.admin_name, self.ctrl_cfg.admin_pswd)
        topo = TopologyInfo(ctrl)
        if(args.switch):
            topo.show_switch(args.switch, args.verbose)
        else:
            topo.show_common(args.verbose)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def show_inv(self, options):
        parser = argparse.ArgumentParser(
            prog=self.prog,
            description='Show topology information',
            usage="%(prog)s show-inv [-s=OPENFLOWID] [-v]"
                   "\n\n"
                  "Show current state of the controller's inventory store\n\n"
                  "  -s   provide information about a given switch\n"
                  "  -v   show detailed information\n")
        parser.add_argument("-v", '--verbose', action="store_true",
                            help="output details level")
        parser.add_argument('-s', '--switch', metavar = "SWITCHID")
        parser.add_argument('-U', action="store_true", dest="usage", help=argparse.SUPPRESS)
        args = parser.parse_args(options)
        if(args.usage):
            parser.print_usage()
            print "\n".strip()
            return
        
        print "TBD (yet to be implemented)"
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def show_flow(self, options):
        parser = argparse.ArgumentParser(
            prog=self.prog,
            description='Show OpenFlow flows information',
            usage="%(prog)s show-flow [-s=OPENFLOWID|--switch=OPENFLOWID]\n"
                  "                        [-t=TABLEID|--table=TABLEID]\n"
                  "                        [-f=FLOWID|--flow=FLOWID]\n"
                  "                        [--cache] [--json]"
                  "\n\n"
                  " Show OpenFlow flows information\n\n"
                  "  -s, --switch  provide information for a given switch\n"
                  "  -t, --table   flow table id\n"
                  "  -f, --flow    flow entry id\n"
                  "  --cache       controller cached flows\n"
                  "  --json        JSON output format\n"
                  )
        parser.add_argument("-v", '--verbose', action="store_true",
                            help="output details level")
        parser.add_argument('-s', '--switch', metavar = "SWITCHID")
        parser.add_argument('-t', '--table', metavar = "TABLEID")
        parser.add_argument('-f', '--flow', metavar = "FLOWID")
        parser.add_argument('-U', action="store_true", dest="usage", help=argparse.SUPPRESS)
        args = parser.parse_args(options)
        if(args.usage):
            parser.print_usage()
            print "\n".strip()
            return
        
        print "TBD (yet to be implemented)"
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def clear_flow(self, options):
        parser = argparse.ArgumentParser(
            prog=self.prog,
            description='Clear OpenFlow flows',
            usage="%(prog)s clear-flow [-s=OPENFLOWID] [-t=TABLEID] [-f=FLOWID]")
        parser.add_argument('-s', '--switch', metavar = "SWITCHID")
        parser.add_argument('-U', action="store_true", dest="usage", help=argparse.SUPPRESS)
        args = parser.parse_args(options)
        if(args.usage):
            parser.print_usage()
            print "\n".strip()
            return
        
        print "TBD (yet to be implemented)"
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def help(self, options):
        parser = argparse.ArgumentParser(add_help=False, 
                                         usage="oftool help <command>")
        parser.add_argument('command')
        args = parser.parse_args(options)
        cmd = args.command.replace('-', '_')
        if not hasattr(self, cmd):
            print 'Unrecognized command %s' % cmd
            return
            
        getattr(self, cmd)(['-U'])
       
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_ctrl_cfg(self, path):
        try:
            with open(path, 'r') as f:
                obj = yaml.load(f)
            d = {}
            for k, v in obj.iteritems():
                d[k] = v
            
            addr = d['ipaddr']
            port = d['port']
            name = d['name']
            pswd = d['pswd']
            cfg = CtrlCfg(addr, port, name, pswd)
            
            return cfg
        except (IOError, KeyError) as e:
            if isinstance(e, IOError):
                print("Error: failed to read file '%s'" % path)
            elif isinstance(e, KeyError):
                print ("Error: unknown attribute %s in file '%s'" % (e, path))
            
            return None

if __name__ == '__main__':
    
    OFToolParser()
