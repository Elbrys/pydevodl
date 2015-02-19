#!/usr/bin/python

import sys
import time
import json
import sys
import xmltodict

from framework.controller import Controller,STATUS,Status

if __name__ == "__main__":

    xmlPayloadTemplate = '''
    <module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
      <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
      <name>{}</name>
      <address xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</address>
      <port xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</port>
      <username xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</username>
      <password xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</password>
      <tcp-only xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">{}</tcp-only>
      <event-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
        <name>global-event-executor</name>
      </event-executor>
      <binding-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
        <name>binding-osgi-broker</name>
      </binding-registry>
      <dom-registry xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
        <name>dom-broker</name>
      </dom-registry>
      <client-dispatcher xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
        <name>global-netconf-dispatcher</name>
      </client-dispatcher>
      <processing-executor xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">prefix:threadpool</type>
        <name>global-netconf-processing-executor</name>
      </processing-executor>
    </module>
    '''
    
#    print xmlPayloadTemplate
#    print type(xmlPayloadTemplate)

    doc = xmltodict.parse(xmlPayloadTemplate)
    print type(doc)
#    print doc
    for key, value in doc.items():
        print "......."
        print key
        print value
        print "......."
#    print json.dumps(doc)
    
    '''
    try:
        schema = doc['get-schema']['output']['data']
        status = STATUS.CTRL_OK
    except (KeyError) as e:
        print "Error: " + repr(e)
    print "TBD: not implemented content type parser"
    '''

    sys.exit(0)




























    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5
    
    print ("\n")
    print ("<<< Creating Controller instance")
    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'    
    time.sleep(rundelay)
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    print ("'Controller':")
    print ctrl.to_json()

   
    print "\n"
    print ("<<< Get list of all YANG models supported by the Controller")
    time.sleep(rundelay)
    nodeName = "controller-config"
    result = ctrl.get_schemas(nodeName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "YANG models list:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)


    print "\n"
    yangModelName = "flow-topology-discovery"
    yangModelVerson = "2013-08-19"
    print ("<<< Retrieve the '%s' YANG model definition from the Controller" % yangModelName)
    time.sleep(rundelay)
    nodeName = "controller-config"
    result = ctrl.get_schema(nodeName, yangModelName, yangModelVerson)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "YANG model definition:"
        schema = result[1]
        print schema
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)
    
    
    print "\n"
    print ("<<< Get list of all service providers available on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_service_providers_info()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        services = result[1]
        print "Services:"
        print json.dumps(services, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    
    print "\n"
    name ="opendaylight-md-sal-binding:binding-data-broker"
    print ("<<< Get '%s' service provider info" % name)
    time.sleep(rundelay)
    result = ctrl.get_service_provider_info(name)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Service:"
        service = result[1]
        print json.dumps(service, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    print "\n"
    print ("<<< Show list of all NETCONF operations supported by the Controller")
    time.sleep(rundelay)
    result = ctrl.get_netconf_operations("controller-config")
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Operations:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

        
    print "\n"
    print ("<<< Show operational state of all configuration modules on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_all_modules_operational_state()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Modules:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    
    print "\n"
    print ("<<< Show operational state of a particular configuration module on the Controller")
    moduleType = "opendaylight-rest-connector:rest-connector-impl"
    moduleName = "rest-connector-default-impl"
    print ("    (module type: %s,\n     module name: %s)"  % (moduleType, moduleName))
    time.sleep(rundelay)
    result = ctrl.get_module_operational_state(moduleType, moduleName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Module:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    
    print "\n"
    print ("<<< Show all sessions running on the Controller ")
    nodeName = "controller-config"
    time.sleep(rundelay)
    result = ctrl.get_sessions_info(nodeName)
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Sessions:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    
    print "\n"
    print ("<<< Show all notification event streams created on the Controller")
    time.sleep(rundelay)
    result = ctrl.get_streams_info()
    status = result[0]
    if (status == STATUS.CTRL_OK):
        print "Streams:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("Demo terminated, reason: %s" % Status(status).string())
        sys.exit(0)

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
