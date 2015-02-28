#!/usr/bin/python

import sys
import time
import json


from framework.controller.controller import Controller
from framework.controller.openflownode import OpenflowNode
from framework.openflowdev.openvswitch.vswitch import VSwitch
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
    
    
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    name = "openflow:1"
    vswitch = VSwitch(ctrl, name)
    
    '''
    result = vswitch.get_switch_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' info:" % name)
        info = result[1]
        print json.dumps(info, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    '''
    
    '''
    print ("\n")
    result = vswitch.get_features_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' features:" % name)
        info = result[1]
        print json.dumps(info, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    '''
    

    '''
    print ("\n")
    result = vswitch.get_ports_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' ports:" % name)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    '''

    '''
    print ("\n")
    portnum = 1
    result = vswitch.get_port_info(portnum)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Port '%s' info:" % portnum)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    '''

    '''
    print ("\n")
    tableid = 0
    result = vswitch.get_flows(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' flows:" % tableid)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    '''

    def getKey(item):
        return item['priority']
    
    print ("\n")
    tableid = 0
    result = vswitch.get_flows_ovs_syntax(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' flows:" % tableid)
        flist = result[1]
        flist.sort(key=getKey)
        for f in flist:
            print json.dumps(f)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)


    '''
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5
    

    print ("\n")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    
    
    print ("\n")
    time.sleep(rundelay)    
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< '%s' added to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONNECTED) == True):
        print ("<<< '%s' is connected to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    yangModelName = "vyatta-security-firewall"
    yangModelVerson = "2014-11-07"
    print ("<<< Retrieve '%s' YANG model definition from the '%s'" % (yangModelName, nodeName))
    time.sleep(rundelay)
    result = vrouter.get_schema(yangModelName, yangModelVerson)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "YANG model definition:"
        schema = result[1]
        print schema
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    '''
    
    
    
