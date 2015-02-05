#!/usr/bin/python

from controller import *
from netconfdev import *
'''
from utils import Status
from utils import CTRL_STATUS
from utils import NODE_STATUS
from utils import check_node_config_status
from utils import check_node_conn_status
from utils import get_all_nodes_in_config
from utils import get_all_nodes_conn_status
'''

if __name__ == "__main__":
    bvcIpAddr =  "172.22.18.245"
#    bvcPortNum = "8181"     
    bvcPortNum = "8080"     
    bvcUname = 'admin' 
    bvcPswd = 'admin'
    nodeName = 'vRouter2'
#    nodeName = 'controller-config'
    
    ctrl = Controller(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd)
    
    '''
    print "\n"
    print ("1) <<< Get all configured nodes >>>")
    result = ctrl.get_all_nodes_in_config()
    status = result[0]
    if (status == CTRL_STATUS.OK):
        print "Nodes configured:"
        nlist = result[1]
        for item in nlist:
            print "   '{}'".format(item)   
    else:
        print ("Error: %s" % Status(status).string())
    '''
    
    '''
    print "\n"
    print ("2) <<< Get connection status for all configured nodes >>>")
    result = ctrl.get_all_nodes_conn_status()
    status = result[0]
    if (status == CTRL_STATUS.OK):
        print "Nodes connection status:"
        nlist = result[1]    
        for item in nlist:
            status = ""
            if (item['connected'] == True):
                status = "connected"
            else:
                status = "disconnected"
            print "   '{}' is {}".format(item['node'], status )
    else:
        print ("Error: %s" % Status(status).string())
    '''
    
    '''
    print "\n"
    print ("3) <<< find a node in config <<<")
    status = ctrl.check_node_config_status(nodeName)
    if (status == NODE_STATUS.CONFIGURED):
        print ("'%s' node is configured" % nodeName)
    elif (status == NODE_STATUS.NOT_FOUND):
        print ("'%s' node is not configured" % nodeName)        
    else:
        print ("Error: %s" % Status(status).string())
    
    print "\n"
    print ("4) >>> get connection status of a node >>>")
    status = ctrl.check_node_conn_status(nodeName)
    if (status == NODE_STATUS.CONNECTED):
        print ("'%s' node is connected" % nodeName)
    elif (status == NODE_STATUS.DISONNECTED):
        print ("'%s' node is not connected" % nodeName)
    elif (status == NODE_STATUS.NOT_FOUND):
        print ("'%s' node is not found" % nodeName)
    else:
        print ("Error: %s" % Status(status).string())
    '''

    '''
    print ("5) >>> get all supported schemas on the 'controller-config"' node>>>")
    result = ctrl.get_all_supported_schemas("controller-config")
    status = result[0]
    if (status == CTRL_STATUS.OK):
        print "Schemas:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Error: %s" % Status(status).string())
    '''

    '''
    print ("6) >>> get schema from the 'controller-config' node>>>")
    result = ctrl.get_schema("controller-config", "opendaylight-inventory", "2013-08-19")
    status = result[0]
    if (status == CTRL_STATUS.OK):
        schema = result[1]
        print schema
    else:
        print ("Error: %s" % Status(status).string())
    '''

    '''
    print ("7) >>> get all supported schemas on the 'vRouter' node>>>")
    result = ctrl.get_all_supported_schemas("vRouter")
    status = result[0]
    if (status == CTRL_STATUS.OK):
        print "Schemas:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Error: %s" % Status(status).string())
    '''

    '''
    print ("8) >>> get schema from the 'vRouter' node>>>")
    result = ctrl.get_schema("vRouter", "vyatta-system-syslog", "2014-10-28")
    status = result[0]
    if (status == CTRL_STATUS.OK):
        schema = result[1]
        print schema
    else:
        print ("Error: %s" % Status(status).string())
    '''
    
    print ("9) >>> add new NETCONF device to the Controller's configuration>>>")
    devName = "vRouter"
    devIpAddr = "172.22.17.107"
    devPortNum = 830
    devUname = "vyatta"
    devPswd = "vyatta"
    tcpOnly="false"
    netconfdev = NetconfDevice(devName, devIpAddr, devPortNum, tcpOnly, devUname, devPswd)
    result = ctrl.add_netconf_node_to_config(netconfdev)
    status = result[0]
    if (status == CTRL_STATUS.OK):
        print "NETCONF device '{}' was successfully mounted on the Controller".format(devName)
    else:
        print ("Error: %s" % Status(status).string())
    
    print ("10) >>> modify configuration of a NETCONF device that does already exist on the Controller>>>")
    netconfdev.devName = "vRouter"
    netconfdev.adminName = "vyatta"
    netconfdev.adminPassword = "vyatta"
    result = ctrl.modify_netconf_node_in_config(netconfdev)
    status = result[0]
    if (status == CTRL_STATUS.OK):
        print "Configuration of NETCONF device '{}' was successfully updated on the Controller".format(devName)
    else:
        print ("Error: %s" % Status(status).string())
    
    
    print ("11) >>> delete NETCONF device from the Controller's configuration>>>")
    result = ctrl.delete_netconf_node_from_config(netconfdev)
    status = result[0]
    if (status == CTRL_STATUS.OK):
        print "Netconf device '{}' was successfully removed from the Controller".format(devName)
    else:
        print ("Error: %s" % Status(status).string())
    
    










    '''
    status = check_node_config_status(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    if (status == NODE_STATUS.CONFIGURED):
        print ("'%s' node is configured" % nodeName)
    elif (status == NODE_STATUS.NOT_FOUND):
        print ("'%s' node is not configured" % nodeName)        
    else:
        print ("Error: %s" % Status(status).string())
    '''
    
    
    
    '''
    url="http://{}:{}/restconf/config/opendaylight-inventory:nodes".format(bvcIpAddr, bvcPortNum)
    res = ctrl_get_request(url, bvcUname, bvcPswd)  
    print type(res)
    status = res[0]
    resp = res[1]
    print status
    print resp
    if (resp != None):
        print resp.status_code
        print resp.content
    '''     
    
    
    '''
    print ("1) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    status = check_node_config_status(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    if (status == NODE_STATUS.CONFIGURED):
        print ("'%s' node is configured" % nodeName)
    elif (status == NODE_STATUS.NOT_FOUND):
        print ("'%s' node is not configured" % nodeName)        
    else:
        print ("Error: %s" % Status(status).string())
    
    print ("2) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    status = check_node_conn_status(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    if (status == NODE_STATUS.CONNECTED):
        print ("'%s' node is connected" % nodeName)
    elif (status == NODE_STATUS.DISONNECTED):
        print ("'%s' node is not connected" % nodeName)
    elif (status == NODE_STATUS.NOT_FOUND):
        print ("'%s' node is not found" % nodeName)
    else:
        print ("Error: %s" % Status(status).string())
    
    print ("3) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    nlist = get_all_nodes_in_config(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    print "Nodes configured:"
    for item in nlist:
        print "   '{}'".format(item)
    
    print ("4) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    nlist = get_all_nodes_conn_status(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd)
    print "Nodes connection status:"
    for item in nlist:
        connstatus = ""
        if (item['connected'] == True):
            connstatus = "connected"
        else:
            connstatus = "disconnected"
        print "   '{}' is {}".format(item['node'], connstatus )
#        print ("'%s' connected %s" % (item['node'], item['connected']))
#        print type(item)
#        print item['node']
#        print item['connected']
#        print "   {}".format(item)

    '''














    
    '''
    print ("1) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    conf_status = get_node_conf_status(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    print conf_status

    print ("2) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    conn_status = get_node_conn_status(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    print conn_status
    
    print ("3) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    nodeslist = get_nodes_config_datastore(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    print "Nodes configured:"
    for item in nodeslist:
        print "   {}".format(item)
   '''
    '''
    capabilities = [
                     "(urn:opendaylight:params:xml:ns:yang:controller:threadpool:impl:fixed?revision=2013-12-01)threadpool-impl-fixed",
                    "(urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom:impl?revision=2013-10-28)opendaylight-sal-dom-broker-impl",
                    "(urn:opendaylight:flow:types:queue?revision=2013-09-25)opendaylight-queue-types"]
   
          
    d = dict()
    d.update({'node': 'vRouter',})
    d.update({'connected': 'True',})
    d.update({'capabilities': capabilities})
    '''
    
    '''
    d = {'node' : 'vRouter',
         'connected' : True,
         'capabilities' : capabilities}
    '''
#    print type(d)
    '''
    for key in d.keys():
        print ("%s: %s" % (key, d[key]))
#        print d[key]
    '''
    
    '''
    print ("4) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    nodeslist = get_nodes_operational_datastore(bvcIpAddr, bvcPortNum, bvcUname, bvcPswd, nodeName)
    print "Nodes operational status:"
    '''