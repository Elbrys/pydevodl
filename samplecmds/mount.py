#!/usr/bin/python

import sys

from framework.controller.controller import Controller
from framework.controller.netconfnode import NetconfNode
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
    node = NetconfNode(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)

    print (">>> Adding '%s' to the Controller '%s'" % (nodeName, ctrlIpAddr))
    result = ctrl.add_netconf_node(node)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' was successfully added to the Controller" % nodeName)
    else:
        print ("Failed, reason: %s" % status.brief().lower())
        sys.exit(0)

    print "\n"
    
