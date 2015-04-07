#!/usr/bin/python

#import sys
import time
import json


from framework.controller.controller import Controller
#from framework.controller.openflownode import OpenflowNode
from framework.openflowdev.ofswitch import OFSwitch
from framework.openflowdev.ofswitch import FlowEntry
from framework.openflowdev.ofswitch import Instruction
from framework.openflowdev.ofswitch import OutputAction
from framework.openflowdev.ofswitch import Match

from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file

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
    node = "openflow:1" # (name:DPID)
    ofswitch = OFSwitch(ctrl, node)

    # --- Flow Match: Ethernet Source Address
    #                 Ethernet  Destination Address
    #                 IPv4 Source Address
    #                 IPv4 Destination Address
    #                 Input Port
    #     NOTE: Ethernet type must be 2048 (0x800) -> IPv4 protocol
    eth_type = 2048
    eth_src = "00:1c:01:00:23:aa"   
    eth_dst = "00:02:02:60:ff:fe"
    ipv4_src = "44.44.44.1/24"
    ipv4_dst = "55.55.55.1/16"
    input_port = 1
         
    print ("<<< 'Controller': %s, 'OpenFlow' switch: '%s'" % (ctrlIpAddr, node))

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
    
    # --- Instruction: 'Apply-action'
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
    status = result[0]
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
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< Flow successfully read from the Controller")
        print ("Flow info:")
        flow = result[1]
        print json.dumps(flow, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
