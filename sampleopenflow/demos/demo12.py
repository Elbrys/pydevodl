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
    #                 Ethernet Destination Address
    #                 ARP Operation
    #                 ARP Source IPv4 Address
    #                 ARP Target IPv4 Address
    #                 ARP source hardware address
    #                 ARP target hardware address
    #     NOTE: Ethernet type MUST be 2054 (0x0806) -> ARP protocol
    eth_type = 2054
    eth_src = "00:ab:fe:01:03:31"
    eth_dst = "ff:ff:ff:ff:ff:ff"
    arp_opcode = 1 # ARP Request
    arp_src_ipv4_addr = "192.168.4.1"
    arp_tgt_ipv4_addr = "10.21.22.23"
    arp_src_hw_addr = "12:34:56:78:98:ab"
    arp_tgt_hw_addr = "fe:dc:ba:98:76:54"
    
    
    print ("<<< 'Controller': %s, 'OpenFlow' switch: '%s'" % (ctrlIpAddr, nodeName))
    
    print "\n"
    print ("<<< Set OpenFlow flow on the Controller")
    print ("        Match:  Ethernet Type (%s)\n"
           "                Ethernet Source Address (%s)\n"
           "                Ethernet Destination Address (%s)\n" 
           "                ARP Operation (%s)\n"
           "                ARP Source IPv4 Address (%s)\n"
           "                ARP Target IPv4 Address (%s)\n"
           "                ARP Source Hardware Address (%s)\n"
           "                ARP Target Hardware Address (%s)"   % (hex(eth_type), eth_src, 
                                                                   eth_dst, arp_opcode,
                                                                   arp_src_ipv4_addr,
                                                                   arp_tgt_ipv4_addr,
                                                                   arp_src_hw_addr,
                                                                   arp_tgt_hw_addr))
    print ("        Action: Output (CONTROLLER)")
    
    
    time.sleep(rundelay)
    
    
    flow_entry = FlowEntry()
    table_id = 0
    flow_entry.set_flow_table_id(table_id)
    flow_id = 19
    flow_entry.set_flow_id(flow_id)
    flow_entry.set_flow_priority(flow_priority = 1010)
    
    # --- Instruction: 'Apply-action'
    #     Action:      'Output' CONTROLLER
    instruction = Instruction(instruction_order = 0)
    action = OutputAction(action_order = 0, port = "CONTROLLER")
    instruction.add_apply_action(action)
    flow_entry.add_instruction(instruction)
    
    # --- Match Fields: Ethernet Type
    #                   Ethernet Source Address
    #                   Ethernet Destination Address
    #                   ARP Operation 
    #                   ARP Source IPv4 Address 
    #                   ARP Target IPv4 Address
    #                   ARP Source Hardware Address
    #                   ARP Target Hardware Address
    match = Match()    
    match.set_eth_type(eth_type)
    match.set_eth_src(eth_src)
    match.set_eth_dst(eth_dst)
    match.set_arp_opcode(arp_opcode)
    match.set_arp_src_transport_address(arp_src_ipv4_addr)
    match.set_arp_tgt_transport_address(arp_tgt_ipv4_addr)
    match.set_arp_src_hw_address(arp_src_hw_addr)
    match.set_arp_tgt_hw_address(arp_tgt_hw_addr)
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
    print ("<<< Delete flow with id of '%s' from the Controller's cache and from the table '%s' on the '%s' node" % (flow_id, table_id, nodeName))
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
    