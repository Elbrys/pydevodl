#!/usr/bin/python

#import sys
import time
import json


from framework.controller.controller import Controller
from framework.openflowdev.ofswitch import OFSwitch
from framework.openflowdev.ofswitch import FlowEntry
from framework.openflowdev.ofswitch import Instruction
from framework.openflowdev.ofswitch import OutputAction, PushVlanHeaderAction, SetFieldAction
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

    # --- Flow Match: Ethernet Type
    #                 VLAN ID
    #                 Input Port
    eth_type = 2048 # IPv4 protocol
    vlan_id = 100
    input_port = 3
    
    # --- Flow Actions: Push VLAN: Ethernet Type
    #                   Set Field: VLAN ID
    #                   Output:    Port Number
    # NOTES:
    #      Ethernet type 33024(0x8100) -> VLAN tagged frame (Customer VLAN Tag Type)
    #      Ethernet type 34984(0x88A8) -> QINQ VLAN tagged frame (Service VLAN tag identifier)
    push_eth_type = 34984
    push_vlan_id = 200
    output_port = 5
    
    print ("<<< 'Controller': %s, 'OpenFlow' switch: '%s'" % (ctrlIpAddr, node))
    
    print "\n"
    print ("<<< Set OpenFlow flow on the Controller")
    print ("        Match:  Ethernet Type (%s)\n"
           "                VLAN ID (%s)\n"
           "                Input Port (%s)\n"              % (hex(eth_type), vlan_id,
                                                               input_port))
    print ("        Actions: 'Push VLAN' (Ethernet Type=%s)"
                                                            % hex(push_eth_type))
    print ("                 'Set Field' (VLAN ID=%s)" % push_vlan_id)
    
    print ("                 'Output' (to Physical Port Number %s)" % output_port)
    
    
    time.sleep(rundelay)
    
    flow_entry = FlowEntry()
    flow_entry.set_flow_name(flow_name = "push_vlan_100_flow")
    table_id = 0
    flow_entry.set_flow_table_id(table_id)
    flow_id = 22
    flow_entry.set_flow_id(flow_id)
    flow_entry.set_flow_priority(flow_priority = 1013)
    flow_entry.set_flow_cookie(cookie = 407)
    flow_entry.set_flow_cookie_mask(cookie_mask = 255)
    flow_entry.set_flow_hard_timeout(hard_timeout = 3400)
    flow_entry.set_flow_idle_timeout(idle_timeout = 3400)
    
    # --- Instruction: 'Apply-action'
    #     Actions:     'PushVlan'
    #                  'SetField'
    #                  'Output'
    instruction = Instruction(instruction_order = 0)
    action = PushVlanHeaderAction(action_order = 0)
    action.set_eth_type(eth_type = push_eth_type)
    instruction.add_apply_action(action)    
    action = SetFieldAction(action_order = 1)
    action.set_vlan_id(vid = push_vlan_id)
    instruction.add_apply_action(action)    
    action = OutputAction(action_order = 2, port = output_port)
    instruction.add_apply_action(action)
    flow_entry.add_instruction(instruction)
    
    # --- Match Fields: Ethernet Type
    #                   Ethernet Source Address
    #                   Ethernet Destination Address
    #                   Input Port
    match = Match()    
    match.set_eth_type(eth_type)
    match.set_vlan_id(vlan_id)
    match.set_in_port(in_port = input_port)
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
