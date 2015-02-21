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
    
    ifName = "dp0p1p7"

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
    print ("<<< Show firewalls configuration of the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result[0]
    if (status.eq(STATUS.OK) == True):
        print ("'%s' firewalls config:" % nodeName)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print "\n"
    fwName1 = "ACCEPT-SRC-IPADDR"
    print (">>> Create new firewall instance '%s' on '%s' " % (fwName1, nodeName))
    time.sleep(rundelay)    
    firewall1 = Firewall()    
    rules = Rules(fwName1)    
    rulenum = 30
    rule = Rule(rulenum)
    rule.add_action("accept")
    rule.add_source_address("172.22.17.108")    
    rules.add_rule(rule)
    firewall1.add_rules(rules)
    result = vrouter.create_firewall_instance(firewall1)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully created" % fwName1)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)

    
    print "\n"
    fwName2 = "DROP-ICMP"
    print (">>> Create new firewall instance '%s' on '%s' " % (fwName2, nodeName))
    time.sleep(rundelay)    
    firewall2 = Firewall()    
    rules = Rules(fwName2)    
    rulenum = 40
    rule = Rule(rulenum)
    rule.add_action("drop")
    rule.add_icmp_typename("ping")
    rules.add_rule(rule)
    firewall2.add_rules(rules)    
    result = vrouter.create_firewall_instance(firewall2)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully created" % fwName2)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        print status.detail()
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Show firewalls configuration of the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result[0]
    if (status.eq(STATUS.OK) == True):
        print ("'%s' firewalls config:" % nodeName)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Apply firewall '%s' to inbound traffic and '%s' to outbound traffic on the '%s' dataplane interface" % (fwName1, fwName2, ifName))
    time.sleep(rundelay)    
    result = vrouter.set_dataplane_interface_firewall(ifName, fwName1, fwName2)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instances were successfully applied to the '%s' dataplane interface" % (ifName))
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName, nodeName))
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
    print (">>> Remove firewall instance '%s' from '%s' " % (fwName1, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall1)  
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully deleted" % fwName1)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)

    
    print "\n"
    print (">>> Remove firewall instance '%s' from '%s' " % (fwName2, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall2)  
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully deleted" % fwName2)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    

    print("\n")
    print ("<<< Show firewalls configuration of the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result[0]
    if (status.eq(STATUS.OK) == True):
        print ("'%s' firewalls config:" % nodeName)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    