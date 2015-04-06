#!/usr/bin/python

import sys
import time
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
    
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5

    print ("\n")
    print ("<<< Creating Controller instance")
    time.sleep(rundelay)
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd, None)
    print ("'Controller':")
    print ctrl.brief_json()
    
    print "\n"
    print ("<<< Get list of OpenFlow nodes connected to the Controller")
    time.sleep(rundelay)
    result = ctrl.get_openflow_nodes_operational_list()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("OpenFlow node names (composed as \"openflow:datapathid\"):")
        nodenames = result[1]
#        for node in nodes:
#            print ("   %s" % node)
        print json.dumps(nodenames, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    print ("<<< Get generic information about OpenFlow nodes")
    time.sleep(rundelay)
    for name in nodenames:
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
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
