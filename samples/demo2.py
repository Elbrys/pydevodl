#!/usr/bin/python

import time

from framework.controller import Controller,STATUS,Status
from framework.netconfnode import *

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
    print ("<<< Created Controller instance: " + ctrl.to_string())

    
    print "\n"
    print ("<<< Show all NETCONF nodes mounted on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Nodes mounted:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Error: %s" % Status(status).string())


    print ("\n")
    time.sleep(rundelay)    
    nodeName = "fake-device"
    nodeIpAddr = "1.2.3.4"
    nodePortNum = 830
    nodeUname = "fake-device-uname"
    nodePswd = "fake-device-pswd"
    print (">>> Creating new '%s' NETCONF node" % nodeName)
    node = NetconfNode(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print (">>> Created NETCONF node : " + node.to_string())    


    print ("\n")
    print (">>> Mount NETCONF node '%s' on the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.add_netconf_node(node)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ">>> NETCONF node '{}' was successfully mounted on the Controller".format(nodeName)
    else:
        print ("Error: %s" % Status(status).string())


    print "\n"
    print ("<<< Show all NETCONF nodes mounted on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Nodes mounted:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Error: %s" % Status(status).string())


    print "\n"
    print ("<<< Find the '%s' NETCONF node on the Controller" % nodeName)
    time.sleep(rundelay)
    status = ctrl.check_node_config_status(nodeName)
    if (status == STATUS.NODE_CONFIGURED):
        print ("'%s' node is mounted" % nodeName)
    elif (status == STATUS.NODE_NOT_FOUND):
        print ("'%s' node is not found" % nodeName)        
    else:
        print ("Error: %s" % Status(status).string())


    print "\n"
    print ("<<< Show connection status for all NETCONF nodes mounted on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_conn_status()
    status = result[0]
    if (status == STATUS.CTRL_OK):
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
        print ("Error: %s" % Status(status).string())


    print "\n"
    print ("<<< Show connection status for the '%s' NETCONF node" % nodeName)
    time.sleep(rundelay)
    status = ctrl.check_node_conn_status(nodeName)
    if (status == STATUS.NODE_CONNECTED):
        print ("'%s' node is connected" % nodeName)
    elif (status == STATUS.NODE_DISONNECTED):
        print ("'%s' node is not connected" % nodeName)
    elif (status == STATUS.NODE_NOT_FOUND):
        print ("'%s' node is not found" % nodeName)
    else:
        print ("Error: %s" % Status(status).string())


    print "\n"
    print (">>> Unmount NETCONF node '%s' from the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.delete_netconf_node(node)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ">>> NETCONF node '{}' was successfully unmounted from the Controller".format(nodeName)
    else:
        print ("Error: %s" % Status(status).string())


    print "\n"
    print ("<<< Show all NETCONF nodes mounted on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Nodes mounted:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Error: %s" % Status(status).string())


    print "\n"
    print ("<<< Get connection status for the '%s' NETCONF node" % nodeName)
    time.sleep(rundelay)
    status = ctrl.check_node_conn_status(nodeName)
    if (status == STATUS.NODE_CONNECTED):
        print ("'%s' node is connected" % nodeName)
    elif (status == STATUS.NODE_DISONNECTED):
        print ("'%s' node is not connected" % nodeName)
    elif (status == STATUS.NODE_NOT_FOUND):
        print ("'%s' node is not found" % nodeName)
    else:
        print ("Error: %s" % Status(status).string())

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
