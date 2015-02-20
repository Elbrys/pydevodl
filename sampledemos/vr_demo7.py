#!/usr/bin/python

import time
import sys
import json

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600 import VRouter5600, Firewall, Rules, Rule
from framework.common.status import STATUS


if __name__ == "__main__":

    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5
    
    print ("\n")
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
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< '%s' added to the Controller" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONNECTED) == True):
        print ("<<< '%s' is connected to the Controller" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    ifName = "dp0p1p7"
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Dataplane interface '%s' config:" % ifName)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print "\n"
    firewallgroup = "FW-ACCEPT-SRC-172_22_17_108"
    firewall = Firewall()    
    rules = Rules(firewallgroup)    
    rulenum = 33
    rule = Rule(rulenum)
    rule.add_action("accept")
    rule.add_source_address("172.22.17.108")    
    rules.add_rule(rule)
    firewall.add_rules(rules)
    print (">>> Create new firewall instance '%s' on '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)    
    result = vrouter.create_firewall_instance(firewall)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully created" % firewallgroup)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Show content of the firewall instance '%s' on '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.get_firewall_instance_cfg(firewallgroup)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s': " % firewallgroup)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Apply '%s' firewall instance to inbound traffic on the '%s' dataplane interface" % (firewallgroup, ifName))
    time.sleep(rundelay)    
    result = vrouter.set_dataplane_interface_inbound_firewall(ifName, firewallgroup)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully applied to inbound traffic on the '%s' dataplane interface" % (firewallgroup, ifName))
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Interfaces '%s' config:" % ifName)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Remove firewall settings from the '%s' dataplane interface" % (ifName))
    time.sleep(rundelay)    
    result = vrouter.delete_dataplane_interface_firewall(ifName)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall settings successfully removed from '%s' dataplane interface" % ifName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Interfaces '%s' config:" % ifName)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print "\n"
    print (">>> Remove firewall instance '%s' from '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall)  
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully deleted" % firewallgroup)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    