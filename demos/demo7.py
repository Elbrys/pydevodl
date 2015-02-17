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
    print (">>> Creating Controller instance")
    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print ("'Controller':")
    print ctrl.to_json()

    print ("\n")
    time.sleep(rundelay)    
    nodeName = "vRouter"
    nodeIpAddr = "172.22.17.107"
    nodePortNum = 830
    nodeUname = "vyatta"
    nodePswd = "vyatta"      
    print (">>> Creating '%s' instance" % nodeName)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print ("'%s':" % nodeName)
    print vrouter.to_json()


    print ("\n")
    print (">>> Add '%s' to the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print (">>> '%s' was successfully added" % (nodeName))
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)


    print "\n"
    print ("<<< Check '%s' configuration status on the Controller" % nodeName)
    time.sleep(rundelay)
    status = ctrl.check_node_config_status(nodeName)
    if (status == STATUS.NODE_CONFIGURED):
        print ("'%s' is configured" % nodeName)
    elif (status == STATUS.NODE_NOT_FOUND):
        print ("'%s' is not found" % nodeName)        
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)


    print "\n"
    print ("<<< Check '%s' connection status on the Controller" % nodeName)
    time.sleep(rundelay)
    status = ctrl.check_node_conn_status(nodeName)
    if (status == STATUS.NODE_CONNECTED):
        print ("'%s' is connected" % nodeName)
    elif (status == STATUS.NODE_DISONNECTED):
        print ("'%s' is not connected" % nodeName)
    elif (status == STATUS.NODE_NOT_FOUND):
        print ("'%s' is not found" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)


    print ("\n")
    print ("<<< Get list of all YANG models supported by the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_schemas()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "YANG models list:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
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
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    print "\n"
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    
    
