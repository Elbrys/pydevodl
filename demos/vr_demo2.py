#!/usr/bin/python

import sys
import time
import json

from framework.controller import Controller, Status, STATUS
from framework.vrouter5600 import VRouter5600

if __name__ == "__main__":

    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5
    

    print ("\n")
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
    print (">>> 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if (status != STATUS.CTRL_OK):
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    status = ctrl.check_node_conn_status(nodeName)
    if (status != STATUS.NODE_CONNECTED):
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    

    print "\n"
    yangModelName = "vyatta-security-firewall"
    yangModelVerson = "2014-11-07"
    print ("<<< Retrieve the '%s' YANG model definition from the '%s'" % (yangModelName, nodeName))
    time.sleep(rundelay)
    result = ctrl.get_schema(nodeName, yangModelName, yangModelVerson)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "YANG model definition:"
        schema = result[1]
        print schema
    else:
        print ("Error: %s" % Status(status).string())

    
    print "\n"
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    
    
