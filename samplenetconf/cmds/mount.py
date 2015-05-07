#!/usr/bin/python

import sys

from framework.controller.controller import Controller
from framework.controller.netconfnode import NetconfNode
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

    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    node = NetconfNode(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)

    print (">>> Adding '%s' to the Controller '%s'" % (nodeName, ctrlIpAddr))
    result = ctrl.add_netconf_node(node)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("'%s' was successfully added to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Failed, reason: %s" % status.brief().lower())
        exit(0)

    print "\n"
    
