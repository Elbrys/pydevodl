#!/usr/bin/python

import sys
import time
import json
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
    print ("<<< Get list of all service providers available on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_service_providers_info()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        services = result[1]
        print "Service providers:"
        print json.dumps(services, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
