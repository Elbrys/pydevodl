#!/usr/bin/python

from framework.controller.controller import Controller
from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file


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
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    
    print "\n"
    print ("<<< Get list of all nodes registered on the Controller")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    result = ctrl.get_nodes_operational_list()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print "Nodes:"
        nlist = result.get_data()
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("\n")
        print ("!!!Failed, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    