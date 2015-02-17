#!/usr/bin/python

import sys
import time
from framework.controller import Controller,STATUS,Status

if __name__ == "__main__":

    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5
    
    print ("\n")
    print ("<<< Creating Controller instance")
    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'    
    time.sleep(rundelay)
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print ("'Controller':")
    print ctrl.to_json()


    print "\n"
    yangModelName = "flow-topology-discovery"
    yangModelVerson = "2013-08-19"
    print ("<<< Retrieve the '%s' YANG model definition from the Controller" % yangModelName)
    time.sleep(rundelay)
    nodeName = "controller-config"
    result = ctrl.get_schema(nodeName, yangModelName, yangModelVerson)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("YANG model:")
        schema = result[1]
        print schema
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
