#!/usr/bin/python

"""
@authors: Sergei Garbuzov

"""

import time
import json

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600 import VRouter5600, Firewall, Rules, Rule
from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file


if __name__ == "__main__":    
    
    f = "cfg4.yml"
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
    
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    
    rundelay = 5
    
    print ("\n")
    
    ifName = "dp0p1p7"
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)    
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.add_netconf_node(vrouter)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("<<< '%s' added to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result.get_status()
    if(status.eq(STATUS.NODE_CONNECTED) == True):
        print ("<<< '%s' is connected to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show firewalls configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result.get_status()
    if (status.eq(STATUS.OK) == True):
        print ("'%s' firewalls config:" % nodeName)
        cfg = result.get_data()
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
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
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully created" % fwName1)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
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
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully created" % fwName2)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        print status.detail()
        exit(0)
    
    
    print("\n")
    print ("<<< Show firewalls configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result.get_status()
    if (status.eq(STATUS.OK) == True):
        print ("'%s' firewalls config:" % nodeName)
        cfg = result.get_data()
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Apply firewall '%s' to inbound traffic and '%s' to outbound traffic on the '%s' dataplane interface" % (fwName1, fwName2, ifName))
    time.sleep(rundelay)    
    result = vrouter.set_dataplane_interface_firewall(ifName, fwName1, fwName2)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instances were successfully applied to the '%s' dataplane interface" % (ifName))
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName, nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Interfaces '%s' config:" % ifName)
        cfg = result.get_data()
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Remove firewall settings from the '%s' dataplane interface" % (ifName))
    time.sleep(rundelay)    
    result = vrouter.delete_dataplane_interface_firewall(ifName)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall settings successfully removed from '%s' dataplane interface" % ifName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Interfaces '%s' config:" % ifName)
        cfg = result.get_data()
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    print (">>> Remove firewall instance '%s' from '%s' " % (fwName1, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall1)  
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully deleted" % fwName1)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    print (">>> Remove firewall instance '%s' from '%s' " % (fwName2, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall2)  
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully deleted" % fwName2)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show firewalls configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result.get_status()
    if (status.eq(STATUS.OK) == True):
        print ("'%s' firewalls config:" % nodeName)
        cfg = result.get_data()
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    print (">>> Remove '%s' NETCONF node from the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.delete_netconf_node(vrouter)
    status = result.get_status()
    if(status.eq(STATUS.OK)):
        print ("'%s' NETCONF node was successfully removed from the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief())        
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    