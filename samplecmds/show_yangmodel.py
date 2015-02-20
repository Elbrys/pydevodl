#!/usr/bin/python

import sys
import getopt
import json

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600  import VRouter5600
from framework.common.status import STATUS

def usage(myname):
    print('   Usage: %s -n <name> -v <version>' % myname)
    sys.exit()

if __name__ == "__main__":
    model_name = None
    model_version = None    

    if(len(sys.argv) == 1):
        print("   Error: missing arguments")
        usage(sys.argv[0])

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"n:v:h",["name=","version=","help"])
    except getopt.GetoptError, e:
        print("   Error: %s" % e.msg)
        usage(sys.argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-n", "--name"):
            model_name = arg
        elif opt in ("-v", "--version"):
            model_version = arg
        else:
            print("Error: failed to parse option %s" % opt)
            usage(sys.argv[0])

    if(model_name == None) or (model_version == None):
        print("Error: incomplete command")
        usage(sys.argv[0])

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
    print ("model name: %s" % model_name)
    print ("model version: %s" % model_version)
    result = vrouter.get_schema(model_name, model_version)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "YANG model definition:"
        schema = result[1]
        print schema
    else:
        print ("Failed, reason: %s" % status.brief().lower())
        print ("%s" % status.detail())
        sys.exit(0)

    print ("\n")
    