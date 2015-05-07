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
    print ("<<< Show firewalls configuration of the '%s'" % nodeName)
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
    firewallgroup = "FW-ACCEPT-SRC-172_22_17_108"
    firewall = Firewall()    
    rules = Rules(firewallgroup)    
    rulenum = 33
    rule = Rule(rulenum)
    rule.add_action("accept")
    rule.add_source_address("172.22.17.108")    
    rules.add_rule(rule)
    firewall.add_rules(rules)
    print ("<<< Create new firewall instance '%s' on '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)    
    result = vrouter.create_firewall_instance(firewall)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully created" % firewallgroup)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show content of the firewall instance '%s' on '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.get_firewall_instance_cfg(firewallgroup)
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s': " % firewallgroup)
        cfg = result.get_data()
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show firewalls configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("'%s' firewalls config:" % nodeName)
        cfg = result.get_data()
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print "\n"
    print ("<<< Remove firewall instance '%s' from '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall)  
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Firewall instance '%s' was successfully deleted" % firewallgroup)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show firewalls configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewalls_cfg()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
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
    