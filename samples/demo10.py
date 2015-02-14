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
    print (">>> Creating Controller instance")
    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print (">>> Created Controller instance: " + ctrl.to_string())

    print ("\n")
    time.sleep(rundelay)    
    nodeName = "vRouter"
    nodeIpAddr = "172.22.17.107"
    nodePortNum = 830
    nodeUname = "vyatta"
    nodePswd = "vyatta"      
    print (">>> Creating new '%s' NETCONF node" % nodeName)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print (">>> Created NETCONF node : " + vrouter.to_string())    


    print ("\n")
    print (">>> Mount NETCONF node '%s' on the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ">>> NETCONF node '{}' was successfully mounted on the Controller".format(nodeName)
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


    print ("\n")
    print ("<<< Get list of all YANG models supported by the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_schemas()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "YANG models list:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Error: %s" % Status(status).string())

    print "\n"
    yangModelName = "vyatta-security-firewall"
    yangModelVerson = "2014-11-07"
    print ("<<< Retrieve the '%s' YANG model definition out of the '%s'" % (yangModelName, nodeName))
    time.sleep(rundelay)
    result = ctrl.get_schema(nodeName, yangModelName, yangModelVerson)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "YANG model definition:"
        schema = result[1]
        print schema
    else:
        print ("Error: %s" % Status(status).string())

    
    print("\n")
    print ("<<< Show Firewall configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewall_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Firewall config:"
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())


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
    print (">>> Create new Firewall instance '%s on '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)    
    result = vrouter.create_firewall_instance(firewall)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully created" % firewallgroup)
#        print ("%s " % firewall.get_payload())
    else:
        print ("Error: %s" % Status(status).string())


    print("\n")
    print ("<<< Show Firewalls configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewall_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Firewall config:"
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())

    print("\n")
    print (">>> Show content of the Firewall instance '%s on '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.get_firewall_instance_cfg(firewallgroup)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s: " % firewallgroup)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())


    print "\n"
    print (">>> Remove Firewall instance '%s' from '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.delete_firewall_instance(firewall)  
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully deleted" % firewallgroup)
    else:
        print ("Error: %s" % Status(status).string())
    

    print("\n")
    print ("<<< Show Firewalls configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_firewall_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Firewalls config:"
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())


    print("\n")
    print (">>> Show content of the Firewall instance '%s on '%s' " % (firewallgroup, nodeName))
    time.sleep(rundelay)
    result = vrouter.get_firewall_instance_cfg(firewallgroup)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s: " % firewallgroup)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())


    print("\n")
    print ("<<< Show Interfaces configuration on the '%s'" % nodeName)
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
        print ("Error: %s" % Status(status).string())


    print("\n")
    ifName = "dp0p1p6"
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
        print ("Error: %s" % Status(status).string())


    
    print "\n"
    print ("tmp run tests terminator")
    sys.exit(0)


    
        
        
    '''
    print("\n")
    result = vrouter.get_firewall_all_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Firewall config:"
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())
    '''
    
        
        
    
    
    
    '''
    print("\n")
    instanceName = "FW-888"
    result = vrouter.get_firewall_instance_cfg(instanceName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s config: " % instanceName)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())
    '''
            
    '''
    print("\n")
    result = vrouter.get_firewall_all_cfg()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Firewall config:"
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("Error: %s" % Status(status).string())
    '''
        
    '''
    print("\n")
    ifName = "dp0p1p7"
    vrouter.apply_firewall_instance_to_interface(ifName, firewallgroup)
    '''
    
    '''
    vrouter.delete_firewall_from_interface(ifName)
    '''
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    
    
