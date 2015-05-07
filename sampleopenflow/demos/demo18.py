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
    
    # --- Flow Match: Ethernet Type
    #                 IPv6 Source Address
    #                 IPv6 Destination Address
    #                 IP DSCP
    #                 TCP Source Port
    #                 TCP Destination Port
    eth_type = ETH_TYPE_IPv6
    ipv6_src = "2001::2acf:e9ff:fe21:6431/80"
    ipv6_dst = "2004:1234:2acf:e9ff::fe21:6431/64"
    ip_dscp = IP_DSCP_CS1 # 'Class Selector' = 'Priority'
    ip_proto = IP_PROTO_TCP
    tcp_src_port = 12345
    tcp_dst_port = 54321
    
    # --- Flow Actions: Output (CONTROLLER)
    output_port = "CONTROLLER"
    
    print ("<<< 'Controller': %s, 'OpenFlow' switch: '%s'" % (ctrlIpAddr, nodeName))
    
    print "\n"
    print ("<<< Set OpenFlow flow on the Controller")
    print ("        Match:  Ethernet Type (%s)\n"
           "                IPv6 Source Address (%s)\n"
           "                IPv6 Destination Address (%s)\n"
           "                IP DSCP (%s)\n"
           "                TCP Source Port (%s)\n"
           "                TCP Destination Port (%s)" % (hex(eth_type), ipv6_src, ipv6_dst,
                                                          ip_dscp, tcp_src_port, tcp_dst_port))
    print ("        Action: Output (to %s)" % output_port)
    
    
    time.sleep(rundelay)
    
    
    flow_entry = FlowEntry()
    flow_entry.set_flow_name(flow_name = "demo18.py")
    table_id = 0
    flow_id = 24
    flow_entry.set_flow_id(flow_id)
    flow_entry.set_flow_priority(flow_priority = 1017)
    
    # --- Instruction: 'Apply-action'
    #     Actions:     'Output'
    instruction = Instruction(instruction_order = 0)
    action = OutputAction(action_order = 0, port = output_port)
    instruction.add_apply_action(action)
    flow_entry.add_instruction(instruction)
    
    # --- Match Fields: Ethernet Type
    #                   IPv6 Source Address
    #                   IPv6 Destination Address
    #                   IP protocol number (TCP)
    #                   IP DSCP
    #                   TCP Source Port
    #                   TCP Destination Port
    match = Match()    
    match.set_eth_type(eth_type)
    match.set_ipv6_src(ipv6_src)
    match.set_ipv6_dst(ipv6_dst)
    match.set_ip_proto(ip_proto)
    match.set_ip_dscp(ip_dscp)
    match.set_tcp_src_port(tcp_src_port)
    match.set_tcp_dst_port(tcp_dst_port)
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
    print ("<<< Delete flow with id of '%s' from the Controller's cache "
           "and from the table '%s' on the '%s' node" % (flow_id, table_id, nodeName))
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
    