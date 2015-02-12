#!/usr/bin/python

import time

from controller import *
from netconfdev import *
from vrouter5600 import *

if __name__ == "__main__":
    bvcIpAddr =  "172.22.18.186"
#    bvcPortNum = "8181"     
    bvcPortNum = "8080"     
    bvcUname = 'admin' 
    bvcPswd = 'admin'
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
    ctrl = Controller(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd)
    print (">>> Created Controller instance: " + ctrl.to_string())

    time.sleep(rundelay)

    netconfdev = NetconfDevice(devName, devIpAddr, devPortNum, tcpOnly, devUname, devPswd)
    print (">>> Created NETCONF node instance: " + netconfdev.to_string())    

    time.sleep(rundelay)

    result = ctrl.add_netconf_node_to_config(netconfdev)
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
    
    vrouter = VRouter5600(ctrl, netconfdev)
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
#    print firewall.to_string()
#    print firewall.to_json()

    groupname = "FW-889"
    rules = Rules(groupname)
    
    rulenum = 33
    rule = Rule(rulenum)
    rule.add_action("accept")
    rule.add_source_address("172.22.17.108")
    
    rules.add_rule(rule)

    firewall.add_rules(rules)
        
#    payload = firewall.get_payload()
#    print payload    
    result = vrouter.create_firewall_instance(firewall)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully created" % groupname)
#        response = result[1]
#        content = response.content
#        print content
    else:
        print ("Error: %s" % Status(status).string())
    
    
    '''
    number = 33
    rule = Rule(number)
    rule.action = "accept"
    rule.source.address = "172.22.17.108"
#    print rule.to_string()
#    print rule.to_json()
    
    print type(firewall.rule)
#    firewall.rule.append(rule)   
#    firewall.rule = rule
    
    firewall.name.append(rule)
    
    
    print firewall.to_json()
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    print("\n")
    fwInstanceName = "FW-889"
    result = vrouter.create_firewall_instance_cfg(fwInstanceName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print ("Firewall instance '%s' was successfully created" % fwInstanceName)
    else:
        print ("Error: %s" % Status(status).string())
        response = result[1]
        if(response):
            print response
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
    instanceName = "FW-888"
    result = vrouter.delete_firewall_instance_cfg(instanceName)  
#    print result      
    status = result[0]
    
    if (status == STATUS.CTRL_OK):
        response = result[1]
        print ("Firewall instance '%s' was successfully deleted" % instanceName)
    else:
        print ("Error: %s" % Status(status).string())
        response = result[1]
        if(response):
            print response
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
    vrouter.apply_firewall_instance_to_interface(ifName, fwInstanceName)
    '''
    
    '''
    vrouter.delete_firewall_from_interface(ifName)
    '''
    

    
    
