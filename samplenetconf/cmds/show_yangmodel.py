#!/usr/bin/python

import sys
import getopt

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600  import VRouter5600
from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file


def usage(myname):
    print('   Usage: %s -i <identifier> -v <version>' % myname)
    sys.exit()

if __name__ == "__main__":
    
    f = "cfg.yml"
    d = {}
    if(load_dict_from_file(f, d) == False):
        print("Config file '%s' read error: " % f)
        exit()

    try:
        ctrlIpAddr = d['ctrlIpAddr']
        ctrlPortNum = d['ctrlPortNum']
        ctrlUname = d['ctrlUname']
        ctrlPswd = d['ctrlPswd']

        nodeName = d['nodeName']
        nodeIpAddr = d['nodeIpAddr']
        nodePortNum = d['nodePortNum']
        nodeUname = d['nodeUname']
        nodePswd = d['nodePswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    model_identifier = None
    model_version = None    

    if(len(sys.argv) == 1):
        print("   Error: missing arguments")
        usage(sys.argv[0])

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"i:v:h",["identifier=","version=","help"])
    except getopt.GetoptError, e:
        print("   Error: %s" % e.msg)
        usage(sys.argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i", "--identifier"):
            model_identifier = arg
        elif opt in ("-v", "--version"):
            model_version = arg
        else:
            print("Error: failed to parse option %s" % opt)
            usage(sys.argv[0])

    if(model_identifier == None) or (model_version == None):
        print("Error: incomplete command")
        usage(sys.argv[0])

    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd) 
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    result = vrouter.get_schema(model_identifier, model_version)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print "YANG model definition:"
        schema = result.get_data()
        print schema
    else:
        print ("\n")
        print ("!!!Failed, reason: %s" % status.brief().lower())
        print ("%s" % status.detailed())
        exit(0)

    print ("\n")
    