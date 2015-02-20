#!/usr/bin/python

import sys
import time
import json

from framework.controller.controller import Controller
from framework.common.status import STATUS


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
    print ("<<< Show operational state of a particular configuration module on the Controller")
    moduleType = "opendaylight-rest-connector:rest-connector-impl"
    moduleName = "rest-connector-default-impl"
    print ("    (module type: %s,\n     module name: %s)"  % (moduleType, moduleName))
    time.sleep(rundelay)
    result = ctrl.get_module_operational_state(moduleType, moduleName)
    status = result[0]
    if(status.eq(STATUS.OK)):
        print "Module:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)

    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
