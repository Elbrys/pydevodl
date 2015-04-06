#!/usr/bin/python

#import sys
#import time
import json


from framework.controller.controller import Controller
#from framework.controller.openflownode import OpenflowNode
from framework.openflowdev.ofswitch import OFSwitch
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
    
    
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    name = "openflow:1"
#    name = "openflow:10195227440578560"
    ofswitch = OFSwitch(ctrl, name)
    
    
    result = ofswitch.get_switch_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' info:" % name)
        info = result[1]
        print json.dumps(info, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    result = ofswitch.get_features_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' features:" % name)
        info = result[1]
        print json.dumps(info, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    
    print ("\n")
    result = ofswitch.get_ports_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' ports:" % name)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
        
    print ("\n")
    portnum = 1
    result = ofswitch.get_port_info(portnum)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Port '%s' info:" % portnum)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    tableid = 0
    result = ofswitch.get_operational_flows(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' operational flows:" % tableid)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    print ("\n")
    tableid = 0
    result = ofswitch.get_operational_flows_ovs_syntax(tableid, sort=True)
    status = result[0]
    
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' operational flows:" % tableid)
        flist = result[1]
        for f in flist:
            print json.dumps(f)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print ("\n")
    tableid = 0
    result = ofswitch.get_configured_flows(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' configured flows:" % tableid)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print ("\n")
    tableid = 0
    result = ofswitch.get_configured_flows_ovs_syntax(tableid, sort=True)
    status = result[0]
    
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' configured flows:" % tableid)
        flist = result[1]
        for f in flist:
            print json.dumps(f)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

