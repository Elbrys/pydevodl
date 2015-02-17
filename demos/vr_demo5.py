#!/usr/bin/python

import time
import sys
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
    
    print("\n")
    print ("<<< Show list of dataplane interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interfaces_list()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Dataplane interfaces:"
        dpIfList = result[1]
        print json.dumps(dpIfList, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    print("\n")
    ifName = "dp0p1p7"
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Dataplane interface '%s' config:" % ifName)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    print("\n")
    print ("<<< Show configuration of dataplane interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interfaces_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Dataplane interfaces config:"
        dpIfCfg = result[1]
        print json.dumps(dpIfCfg, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
