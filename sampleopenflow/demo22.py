#!/usr/bin/python

import time
import json


from framework.controller.controller import Controller
from framework.openflowdev.ofswitch import OFSwitch
from framework.openflowdev.ofswitch import FlowEntry
from framework.openflowdev.ofswitch import Instruction
from framework.openflowdev.ofswitch import OutputAction
from framework.openflowdev.ofswitch import PushMplsHeaderAction
from framework.openflowdev.ofswitch import SetFieldAction
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

    # --- Flow Match: Ethernet Type
    #                 Input Port
    #                 IPv4 Destination Address
    eth_type = 34887 # MPLS unicast (0x8847)
    in_port = 1
    ipv4_dst = "10.12.5.4/32"
    
    # --- Flow Actions: Push MPLS
    #                   Set Field
    #                   Output
    push_ether_type = 34887 # MPLS unicast (0x8847)
    mpls_label = 27
    output_port = 2
    
    print ("<<< 'Controller': %s, 'OpenFlow' switch: '%s'" % (ctrlIpAddr, nodeName))
    
    print "\n"
    print ("<<< Set OpenFlow flow on the Controller")
    print ("        Match:  Ethernet Type (%s)\n"
           "                Input Port (%s)\n"
           "                IPv4 Destination Address (%s)"% (hex(eth_type), in_port, ipv4_dst))
    print ("        Actions: 'Output' (Physical Port number %s)" % output_port)
    
    
    time.sleep(rundelay)
    
    
    flow_entry = FlowEntry()
    table_id = 0
    flow_id = 28
    flow_entry.set_flow_name(flow_name = "Push MPLS Label")
    flow_entry.set_flow_id(flow_id )
    flow_entry.set_flow_priority(flow_priority = 1021)
    flow_entry.set_flow_cookie(cookie = 654)
    flow_entry.set_flow_cookie_mask(cookie_mask = 255)
    
    # --- Instruction: 'Apply-action'
    #     Actions:     'Push MPLS Header'
    #                  'Set Field'
    #                  'Output'
    instruction = Instruction(instruction_order = 3)
    action = PushMplsHeaderAction(action_order = 0)
    action.set_eth_type(push_ether_type)
    instruction.add_apply_action(action)        
    action = SetFieldAction(action_order = 1)
    action.set_mpls_label(mpls_label)
    instruction.add_apply_action(action)    
    action = OutputAction(action_order = 2, port = output_port)
    instruction.add_apply_action(action)
    flow_entry.add_instruction(instruction)
    
    # --- Match Fields: Ethernet Type
    #                   Input Port
    #                   IPv4 Destination Address
    match = Match()    
    match.set_eth_type(eth_type)
    match.set_in_port(in_port)
    match.set_ipv4_dst(ipv4_dst)
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
        print ("!!!Demo terminated, reason: %s" % status.detail())
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
    print ("<<< Delete flow with id of '%s' from the Controller's cache "
           "and from the table '%s' on the '%s' node" % (flow_id, table_id, nodeName))
    time.sleep(rundelay)
    result = ofswitch.delete_flow(flow_entry.get_flow_table_id(), flow_entry.get_flow_id())
    status = result[0]
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
    