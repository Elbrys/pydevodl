#!/usr/bin/python

#import sys
import time
import json


from framework.controller.controller import Controller
#from framework.controller.openflownode import OpenflowNode
from framework.openflowdev.ofswitch import OFSwitch
from framework.openflowdev.ofswitch import FlowEntry
from framework.openflowdev.ofswitch import Instruction
from framework.openflowdev.ofswitch import DropAction
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
    ofswitch = "openflow:1"
    ofswitch = OFSwitch(ctrl, ofswitch)

    # OpenFlow flow attributes
    table_id = 0
    flow_id = 12
    flow_priority = 1000
    eth_type = 2048
    ipv4_src = "10.11.12.13/24"
        
            
    print ("<<< 'Controller': %s, OpenFlow switch (name:DPID)'%s'" % (ctrlIpAddr, ofswitch))

    print "\n"
    print ("<<< Set OpenFlow flow on the Controler")
    print ("        Match:  Ethernet Type (%s),\n"
           "                IPv4 Source Address (%s)" % (hex(eth_type), ipv4_src))
    print ("        Action: Drop")

    time.sleep(rundelay)
    
    
    flow_entry = FlowEntry()
    flow_entry.set_flow_id(flow_id)
    flow_entry.set_flow_priority(flow_priority)
    
    instruction = Instruction(instruction_order = 0)    
    action = DropAction(action_order = 0)    
    instruction.add_apply_action(action)
    flow_entry.add_instruction(instruction)
    
    match = Match()
    match.set_eth_type(eth_type)     
    match.set_ipv4_src(ipv4_src)       
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
