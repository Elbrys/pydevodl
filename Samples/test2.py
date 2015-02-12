#!/usr/bin/python

import time
import sys
from controller import *
from netconfdev import *
from vrouter5600 import *

if __name__ == "__main__":
    
    interface = InterfaceDataplane("dp0p1p7")
    inFwName= "FW-889"
    interface.add_in_firewall(inFwName);
    
    '''
    
    fw = InterfaceDataplaneFirewall()
    
    firewallgroup = "FW-889"
    inputFwName = "FW-889"
    fw.add_in_item(inputFwName)
    
    interface.add_firewall(fw)
    '''
    

#    print interface.to_json()
    s = interface.to_payload()
    sys.exit(0)
    print ("222")
    
    
    ctrlIpAddr =  "172.22.18.186"
#    bvcPortNum = "8181"     
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'
#    nodeName = 'vRouter2'
#    nodeName = 'controller-config'

    devName = "vRouter"
    devIpAddr = "172.22.17.107"
    devPortNum = 830
    devUname = "vyatta"
    devPswd = "vyatta"
    tcpOnly="false"
    
    rundelay = 2
    
    print (">>> Demo started")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print (">>> Created Controller instance: " + ctrl.to_string())

    time.sleep(rundelay)

    node = NetconfDevice(devName, devIpAddr, devPortNum, tcpOnly, devUname, devPswd)
    print (">>> Created NETCONF node instance: " + node.to_string())    

    time.sleep(rundelay)

    result = ctrl.add_netconf_node_to_config(node)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ">>>NETCONF node '{}' was successfully mounted on the Controller".format(devName)
    else:
        print ("Error: %s" % Status(status).string())

    time.sleep(rundelay)
    
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
    
    vrouter = VRouter5600(ctrl, node)
    print vrouter.to_string()
    print (">>> Created vRouter: " + vrouter.to_string())
    
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
    
    
    firewall = Firewall()
    
    firewallgroup = "FW-889"
    rules = Rules(firewallgroup)
    
    rulenum = 33
    rule = Rule(rulenum)
    rule.add_action("accept")
    rule.add_source_address("172.22.17.108")
    
    rules.add_rule(rule)

    firewall.add_rules(rules)
        
    result = vrouter.create_firewall_instance(firewall)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully created" % firewallgroup)
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
    

    
    
