#!/usr/bin/python

import sys
import time
import json
from framework.controller import Controller
from framework.status import STATUS

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
    print ("<<< Get list of all YANG models supported by the Controller")
    time.sleep(rundelay)
    nodeName = "controller-config"
    result = ctrl.get_schemas(nodeName)
    status = result[0]
    if(status.eq(STATUS.OK)):
        print "YANG models list:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
