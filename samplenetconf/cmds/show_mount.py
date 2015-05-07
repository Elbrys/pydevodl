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

        nodeName = d['nodeName']
        nodeIpAddr = d['nodeIpAddr']
        nodePortNum = d['nodePortNum']
        nodeUname = d['nodeUname']
        nodePswd = d['nodePswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    
    print "\n"
    print ("<<< NETCONF nodes configured on the Controller")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    result = ctrl.get_all_nodes_in_config()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print "Nodes configured:"
        nlist = result.get_data()
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("\n")
        print ("!!!Failed, reason: %s" % status.brief().lower())
        exit(0)
  
    print "\n"
    print ("<<< NETCONF nodes connection status on the Controller")
    result = ctrl.get_all_nodes_conn_status()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print "Nodes connection status:"
        nlist = result.get_data()
        for item in nlist:
            status = ""
            if (item['connected'] == True):
                status = "connected"
            else:
                status = "not connected"
            print "   '{}' is {}".format(item['node'], status )
    else:
        print ("Failed, reason: %s" % status.brief().lower())
        exit(0)
        
    print "\n"
    