#!/usr/bin/python

import time
import sys

from framework.controller import *
from framework.netconfnode import *
from framework.vrouter5600 import *

if __name__ == "__main__":

    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'

    nodeName = "vRouter"
    nodeIpAddr = "172.22.17.107"
    nodePortNum = 830
    nodeUname = "vyatta"
    nodePswd = "vyatta"
#    nodeTcpOnly="false"
  
    rundelay = 2

    print (">>> Demo started")
    
    print ("\n")
    print (">>> Creating Controller instance")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print (">>> Created Controller instance: " + ctrl.to_string())

    print ("\n")
    print (">>> Creating NETCONF node")
    time.sleep(rundelay)    
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print (">>> Created NETCONF node : " + vrouter.to_string())    

    print ("\n")
    print (">>> Mounting NETCONF node '%s' on the Controller" % nodeName)
    time.sleep(rundelay)    
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ">>> NETCONF node '{}' was successfully mounted on the Controller".format(nodeName)
    else:
        print ("Error: %s" % Status(status).string())

    print ("\n")
    print (">>> Getting list of schemas supported by '%s' " + nodeName)
    time.sleep(rundelay)
    result = vrouter.get_schemas()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Schemas:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Error: %s" % Status(status).string())


    '''
    nodes = ctrl.get_all_nodes()
    for node in nodes:
#        print type(node)
        if isinstance(node, NetconfNode):
            print"ppppp"
            print node
            if(isinstance(node, VRouter5600)):
               print"ppppp"
               print type(node)
               print node.to_string()

    '''
    
    '''
    node = NetconfNode(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    node.add_device(vrouter)
    
    
#    vrouter = VRouter5600(ctrl, node)
#    node.add_device(vrouter)    
    ctrl.add_node(node)
    
    nodes = ctrl.get_all_nodes()
    for node in nodes:
        print type(node)
        if isinstance(node, NetconfNode):
            print node.to_string()
    
    
    node = ctrl.get_node(nodeName)
    if (node != None):
        print node.to_string()
    
    sys.exit(0)
    '''
    
    '''
    ifName = "dp0p1p7"
    fwobj = InterfaceDataplaneFirewall(ifName)
    inFw = "FW-888"
    fwobj.add_in_item(inFw)
    print fwobj.get_payload()
    
    result = vrouter.apply_firewall_to_dataplane_interface(fwobj)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print("Firewall '%s' successfully applied to the dataplane interface '%s'" % (inFw, ifName))
    else:
        print ("Error: %s" % Status(status).string())
    '''
    
    '''
    print (">>> Demo started")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print (">>> Created Controller instance: " + ctrl.to_string())

    time.sleep(rundelay)

    time.sleep(rundelay)

    result = ctrl.add_netconf_node_to_config(node)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ">>>NETCONF node '{}' was successfully mounted on the Controller".format(devName)
    else:
        print ("Error: %s" % Status(status).string())

    time.sleep(rundelay)
    '''
    
    '''
    status = ctrl.check_node_config_status(netconfdev.devName)
    if (status == STATUS.NODE_NOT_FOUND):
        print ("'%s' node is not configured" % netconfdev.devName)        
        print ("Adding '%s' node to the Controller's configuration>>>" % netconfdev.devName)
        result = ctrl.add_netconf_node_to_config(netconfdev)
        status = result[0]
        if (status == STATUS.CTRL_OK):
            print "'{}' was successfully configured on the Controller".format(devName)
        else:
            print ("Error: %s" % Status(status).string())
    elif (status == STATUS.NODE_CONFIGURED):
        print ("'%s' node is configured on the Controller" % netconfdev.devName)
    else:
        print ("Error: %s" % Status(status).string())
    '''

    '''
    vrouter = VRouter5600(ctrl, node)
    print vrouter.to_string()
    print (">>> Created vRouter: " + vrouter.to_string())
    '''
    
    '''
    result = vrouter.get_schemas()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Schemas:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Error: %s" % Status(status).string())
    '''
    
    '''
    result = vrouter.get_schema("vyatta-security-firewall", "2014-11-07")
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Schema:"
        schema = result[1]
        print schema
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
    
    print "\n"
    firewallgroup = "FW-889"
    time.sleep(rundelay)    
    firewall = Firewall()    
    rules = Rules(firewallgroup)    
    rulenum = 33
    rule = Rule(rulenum)
    rule.add_action("accept")
    rule.add_source_address("172.22.17.108")    
    rules.add_rule(rule)
    firewall.add_rules(rules)
    print (">>> Creating new firewall instance '%s on '%s' " % (firewallgroup, nodeName))
    result = vrouter.create_firewall_instance(firewall)
    status = result[0]
    if (status == STATUS.CTRL_OK):
#        print ("Firewall instance '%s' was successfully created" % firewallgroup)
        print ("Firewall instance '%s' was successfully created:" % firewallgroup)
        print ("%s " % firewall.get_payload())
    else:
        print ("Error: %s" % Status(status).string())


        
        
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
    
        
        
    print "\n"
    print (">>> Removing firewall instance '%s' from '%s' " % (firewallgroup, nodeName))
    result = vrouter.delete_firewall_instance(firewall)  
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully deleted" % firewallgroup)
    else:
        print ("Error: %s" % Status(status).string())
    
    
    
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
    

    
    
