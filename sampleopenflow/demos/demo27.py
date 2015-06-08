#!/usr/bin/python

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

import time
import json


from framework.controller.controller import Controller
from framework.controller.topology import Topology
from framework.openflowdev.ofswitch import OFSwitch
from framework.openflowdev.ofswitch import FlowEntry
from framework.openflowdev.ofswitch import Instruction
from framework.openflowdev.ofswitch import OutputAction
from framework.openflowdev.ofswitch import Match

from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file
from framework.common.constants import *

if __name__ == "__main__":
    
    f = "cfg.yml"
    d = {}
    if(load_dict_from_file(f, d) == False):
        print("Config file '%s' read error: " % f)
        exit()
    
    try:
        ctrlIpAddr = d['ctrlIpAddr']
        ctrlPortNum = d['ctrlPortNum']
        ctrlUname = d['ctrlUname']
        ctrlPswd = d['ctrlPswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    
    rundelay = 5
    
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    
    print "\n"
    print ("<<< Controller '%s:%s" % (ctrlIpAddr, ctrlPortNum))
    time.sleep(rundelay)
    
    
    print ("\n")
    print ("<<< OpenFlow summary information")
   
    topologies = []
    flows_cnt = 0
    num_of_switches = 0
    num_of_inter_switch_links = 0
    num_of_hosts = 0
    
    result = ctrl.get_openflow_operational_flows_total_cnt()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        flows_cnt  = result.get_data()
        assert(isinstance(flows_cnt, int))
    else:
        print ("\n")
        print ("!!!Error, failed to get OpenFlow flows count, reason: %s" 
               % status.brief().lower())
        exit(0)
    
    result = ctrl.get_topology_names()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        tnames = result.get_data()
        assert(isinstance(tnames, list))
    else:
        print ("\n")
        print ("!!!Error, failed to get topology info, reason: %s" % status.brief().lower())
        exit(0)
    
    
    for item in tnames:
        result = ctrl.build_topology_object(item)
        status = result.get_status()
        if(status.eq(STATUS.OK) == True):
            topo  = result.get_data()
            topologies.append(topo)
            assert(isinstance(topo, Topology))
            num_of_switches += topo.get_switches_cnt()
            num_of_inter_switch_links += topo.get_inter_switch_links_cnt()
            num_of_hosts += topo.get_hosts_cnt()
        else:
            print ("\n")
            print ("!!!Error, failed to parse '%s' topology info, reason: %s" 
                   % (item, status.brief().lower()))
            exit(0)
    
    
    print "    Number of network topologies: %s" % len(tnames)
    print "    Number of switches:           %s" % num_of_switches
    print "    Number of inter switch links: %s" % num_of_inter_switch_links
    print "    Number of operational flows:  %s" % flows_cnt
    print "    Number of hosts:              %s" % num_of_hosts
    
    
    time.sleep(rundelay)
    
    
    print "\n"
    print ("<<< Network topology identifiers:")
    for topo in topologies:
        print ("    '%s'") % topo.topology_id
    
    
    time.sleep(rundelay)
    
    
    for topo in topologies:
        print "\n"
        print ("<<< Topology '%s' summary information:") % topo.topology_id
        print ("    Number of switches: %s" % topo.get_switches_cnt())
        print ("    Number of inter switch links: %s" % topo.get_inter_switch_links_cnt())
        print ("    Number of hosts: %s" % topo.get_hosts_cnt())
        print "\n"
    
    
    time.sleep(rundelay)
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
