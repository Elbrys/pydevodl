#!/usr/bin/python

import sys
import json

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600  import VRouter5600
from framework.common.status import STATUS

if __name__ == "__main__":
    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)

    nodeName = "vRouter"
    nodeIpAddr = "172.22.17.107"
    nodePortNum = 830
    nodeUname = "vyatta"
    nodePswd = "vyatta"      
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd) 
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    
    result = vrouter.get_loopback_interfaces_list()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Loopback interfaces:"
        dpIfList = result[1]
        print json.dumps(dpIfList, indent=4)
    else:
        print ("Failed, reason: %s" % status.brief().lower())
        sys.exit(0)
