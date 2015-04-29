#!/usr/bin/python

import sys
import json

from framework.controller.controller import Controller
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

        nodeId = "openflow:2"
#        nodeId = "vRouter"
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    
    print "\n"
    print ("<<< Get info about '%s' node on the Controller" % nodeId)
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    result = ctrl.get_node_info(nodeId)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' node info:" % nodeId)
        info = result[1]
#        print info
        print json.dumps(info, indent=4)
#        for item in nlist:
#            print "   '{}'".format(item)   
    else:
        print ("\n")
        print ("!!!Failed, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    