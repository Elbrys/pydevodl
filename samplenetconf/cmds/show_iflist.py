#!/usr/bin/python

import sys
import json

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600  import VRouter5600
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
        nodeIpAddr = d['nodeIpAddr']
        nodePortNum = d['nodePortNum']
        nodeUname = d['nodeUname']
        nodePswd = d['nodePswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)

    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd) 
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    
    result = vrouter.get_interfaces_list()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print "Interfaces:"
        ifList = result.get_data()
        print json.dumps(ifList, indent=4)
    else:
        print ("\n")
        print ("!!!Failed, reason: %s" % status.brief().lower())
        print ("%s" % status.detailed())
        sys.exit(0)
    