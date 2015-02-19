#!/usr/bin/python

import sys
import time
import os

from framework.controller import Controller
from framework.status import STATUS
from framework.netconfnode import NetconfNode

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
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print ("'Controller':")
    print ctrl.to_json()

    
    print "\n"
    print ("<<< Show NETCONF nodes configured on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if(status.eq(STATUS.OK)):
        print "Nodes configured:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)


    print ("\n")
    time.sleep(rundelay)    
    nodeName = "dut-device"
    nodeIpAddr = "172.22.17.107"
    nodePortNum = 830
    nodeUname = "vyatta"
    nodePswd = "vyatta"
    print ("<<< Creating new '%s' NETCONF node" % nodeName)
    node = NetconfNode(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print ("'%s':" % nodeName)
    print node.to_json()


    print ("\n")
    print ("<<< Check '%s' NETCONF node availability on the network" % nodeName)
    time.sleep(rundelay)
    response = os.system("ping -c 1 " + nodeIpAddr)

    if response == 0:
        print nodeIpAddr, 'is up!'
    else:
        print nodeIpAddr, 'is down!'
        print ("Demo terminated")
        sys.exit(0)

    print ("\n")
    print ("<<< Add '%s' NETCONF node to the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.add_netconf_node(node)
    status = result[0]
    if(status.eq(STATUS.OK)):
        print ("'%s' NETCONF node was successfully added to the Controller" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)
    

    print "\n"
    print ("<<< Show NETCONF nodes configured on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if(status.eq(STATUS.OK)):
        print "Nodes configured:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)


    print "\n"
    print ("<<< Find the '%s' NETCONF node on the Controller" % nodeName)
    time.sleep(rundelay)
    result = ctrl.check_node_config_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONFIGURED)):
        print ("'%s' node is configured" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)
    
    
    print "\n"
    print ("<<< Show connection status for all NETCONF nodes configured on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_conn_status()
    status = result[0]
    if(status.eq(STATUS.OK)):
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
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)


    print "\n"
    print ("<<< Show connection status for the '%s' NETCONF node" % nodeName)
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONNECTED)):
        print ("'%s' node is connected" % nodeName)
    elif (status.eq(STATUS.NODE_DISONNECTED)):
        print ("'%s' node is not connected" % nodeName)
    elif (status.eq(STATUS.NODE_NOT_FOUND)):
        print ("'%s' node is not found" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)
    
    
    print "\n"
    print (">>> Remove '%s' NETCONF node from the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.delete_netconf_node(node)
    status = result[0]
    if(status.eq(STATUS.OK)):
        print ("'%s' NETCONF node was successfully removed from the Controller" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)
    

    print "\n"
    print ("<<< Show NETCONF nodes configured on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if(status.eq(STATUS.OK)):
        print "Nodes configured:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)
    

    print "\n"
    print ("<<< Show connection status for the '%s' NETCONF node" % nodeName)
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONNECTED)):
        print ("'%s' node is connected" % nodeName)
    elif (status.eq(STATUS.NODE_DISONNECTED)):
        print ("'%s' node is not connected" % nodeName)
    elif (status.eq(STATUS.NODE_NOT_FOUND)):
        print ("'%s' node is not found" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())        
        sys.exit(0)
    

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
