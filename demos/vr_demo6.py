#!/usr/bin/python

import time
import sys

from framework.controller import *
from framework.netconfnode import *
from framework.vrouter5600 import *

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
    print (">>> 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if (status != STATUS.CTRL_OK):
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    status = ctrl.check_node_conn_status(nodeName)
    if (status != STATUS.NODE_CONNECTED):
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    print("\n")
    print ("<<< Show list of loopback interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_loopback_interfaces_list()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Loopback interfaces:"
        dpIfList = result[1]
        print json.dumps(dpIfList, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    print("\n")
    ifName = "lo4"
    print ("<<< Show '%s' loopback interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_loopback_interface_cfg(ifName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Loopback interface '%s' config:" % ifName)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Show configuration of loopback interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_loopback_interfaces_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Loopback interfaces config:"
        lbIfCfg = result[1]
        print json.dumps(lbIfCfg, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
        
    print("\n")
    print ("<<< Show interfaces configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_interfaces_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Interfaces config:"
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)


    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

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
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully created" % firewallgroup)
#        print ("%s " % firewall.get_payload())
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)


    print("\n")
#    ifName = "dp0p1p7"
    print ("<<< Apply '%s' firewall instance to inbound traffic on the '%s' dataplane interface" % (firewallgroup, ifName))
    time.sleep(rundelay)    
    result = vrouter.set_dataplane_interface_inbound_firewall(ifName, firewallgroup)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully applied to inbound traffic on the '%s' dataplane interface" % (firewallgroup, ifName))
#        print ("%s " % firewall.get_payload())
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)


    print("\n")
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Interfaces '%s' config:" % ifName)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Remove firewall settings from the '%s' dataplane interface" % (ifName))
    time.sleep(rundelay)    
    result = vrouter.delete_dataplane_interface_firewall(ifName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall settings successfully removed from '%s' dataplane interface" % ifName)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
        
    print("\n")
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Interfaces '%s' config:" % ifName)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    
    print "\n"
    print (">>> Remove firewall instance '%s' from '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall)  
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully deleted" % firewallgroup)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    
    