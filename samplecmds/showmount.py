#!/usr/bin/python

import sys

from framework.controller.controller import Controller
from framework.common.status import STATUS


if __name__ == "__main__":

    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)

    print "\n"
    print ("<<< NETCONF nodes configured on the Controller")
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Nodes configured:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Failed, reason: %s" % status.brief().lower())
        sys.exit(0)
  
    print "\n"
    print ("<<< NETCONF nodes connection status on the Controller")
    result = ctrl.get_all_nodes_conn_status()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Nodes connection status:"
        nlist = result[1]    
        for item in nlist:
            status = ""
            if (item['connected'] == True):
                status = "connected"
            else:
                status = "not connected"
            print "   '{}' is {}".format(item['node'], status )
    else:
        print ("Failed, reason: %s" % status.brief().lower())
        sys.exit(0)
        
    print "\n"

   