#!/usr/bin/python

"""
@authors: Sergei Garbuzov

"""

import time
import json


from framework.controller.controller import Controller
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
        nodeName = d['nodeName']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    
    rundelay = 5
    
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    ofswitch = OFSwitch(ctrl, nodeName)
    
    # --- Flow Match: Ethernet Source Address
    #                 Ethernet  Destination Address
    #                 IPv4 Source Address
    #                 IPv4 Destination Address
    #                 Input Port
    #     NOTE: Ethernet type must be 2048 (0x800) -> IPv4 protocol
    eth_type = ETH_TYPE_IPv4
    eth_src = "00:1a:1b:00:22:aa"   
    eth_dst = "00:2b:00:60:ff:f1"
    ipv4_src = "44.44.44.1/24"
    ipv4_dst = "55.55.55.1/16"
    input_port = 13
    
    print ("<<< 'Controller': %s, 'OpenFlow' switch: '%s'" % (ctrlIpAddr, nodeName))
    
    print "\n"
    print ("<<< Set OpenFlow flow on the Controller")
    print ("        Match:  Ethernet Type (%s)\n"
           "                Ethernet Source Address (%s)\n"
           "                Ethernet Destination Address (%s)\n" 
           "                IPv4 Source Address (%s)\n"
           "                IPv4 Destination Address (%s)\n" 
           "                Input Port (%s)"               % (hex(eth_type), eth_src, 
                                                              eth_dst, ipv4_src, ipv4_dst,
                                                              input_port))
    print ("        Action: Output (CONTROLLER)")
    
    
    time.sleep(rundelay)
    
    
    flow_entry = FlowEntry()
    table_id = 0
    flow_entry.set_flow_table_id(table_id)
    flow_id = 15
    flow_entry.set_flow_id(flow_id)
    flow_entry.set_flow_priority(flow_priority = 1005)
    
    # --- Instruction: 'Apply-actions'
    #     Action:      'Output' to CONTROLLER
    instruction = Instruction(instruction_order = 0)
    action = OutputAction(action_order = 0, port = "CONTROLLER", max_len=60)
    instruction.add_apply_action(action)    
    flow_entry.add_instruction(instruction)
    
    
    #--- Match Fields: Ethernet Type
    #                  Ethernet Source Address
    #                  Ethernet Destination Address
    #                  IPv4 Source Address
    #                  IPv4 Destination Address
    #                  Input Port    
    match = Match()
    match.set_eth_type(eth_type)
    match.set_eth_src(eth_src)    
    match.set_eth_dst(eth_dst)
    match.set_ipv4_src(ipv4_src)
    match.set_ipv4_dst(ipv4_dst)
    match.set_in_port(input_port)
    flow_entry.add_match(match)
    
    
    print ("\n")
    print ("<<< Flow to send:")
    print flow_entry.get_payload()
    time.sleep(rundelay)
    result = ofswitch.add_modify_flow(flow_entry)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("<<< Flow successfully added to the Controller")
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")    
    print ("<<< Get configured flow from the Controller")    
    time.sleep(rundelay)
    result = ofswitch.get_configured_flow(table_id, flow_id)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("<<< Flow successfully read from the Controller")
        print ("Flow info:")
        flow = result.get_data()
        print json.dumps(flow, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print ("<<< Delete flow with id of '%s' from the Controller's cache and from the table '%s' on the '%s' node" % (flow_id, table_id, nodeName))
    time.sleep(rundelay)
    result = ofswitch.delete_flow(flow_entry.get_flow_table_id(), flow_entry.get_flow_id())
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("<<< Flow successfully removed from the Controller")
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    