#!/usr/bin/python

# Copyright (c) 2015,  BROCADE COMMUNICATIONS SYSTEMS, INC

# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

"""

@authors: Sergei Garbuzov
@status: Development
@version: 1.1.0


"""

import time
import json

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600 import VRouter5600
from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file


if __name__ == "__main__":

    f = "cfg4.yml"
    d = {}
    if(load_dict_from_file(f, d) is False):
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
        ifName = d['loopback']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)

    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 3

    print ("\n")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum,
                          nodeUname, nodePswd)
    print ("<<< 'Controller': %s, '%s': %s"
           % (ctrlIpAddr, nodeName, nodeIpAddr))

    print ("\n")
    time.sleep(rundelay)
    node_configured = False
    result = ctrl.check_node_config_status(nodeName)
    status = result.get_status()
    if(status.eq(STATUS.NODE_CONFIGURED)):
        node_configured = True
        print ("<<< '%s' is configured on the Controller" % nodeName)
    elif(status.eq(STATUS.DATA_NOT_FOUND)):
        node_configured = False
    else:
        print ("\n")
        print "Failed to get configuration status for the '%s'" % nodeName
        print ("!!!Demo terminated, reason: %s" % status.detailed())
        exit(0)

    if node_configured is False:
        result = ctrl.add_netconf_node(vrouter)
        status = result.get_status()
        if(status.eq(STATUS.OK)):
            print ("<<< '%s' added to the Controller" % nodeName)
        else:
            print ("\n")
            print ("!!!Demo terminated, reason: %s" % status.detailed())
            exit(0)

    print ("\n")
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result.get_status()
    if(status.eq(STATUS.NODE_CONNECTED)):
        print ("<<< '%s' is connected to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print("\n")
    print ("<<< Show list of loopback interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_loopback_interfaces_list()
    status = result.get_status()
    if(status.eq(STATUS.OK)):
        print "Loopback interfaces:"
        dpIfList = result.get_data()
        print json.dumps(dpIfList, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print("\n")
    print ("<<< Show '%s' loopback interface configuration on the '%s'"
           % (ifName, nodeName))
    time.sleep(rundelay)
    result = vrouter.get_loopback_interface_cfg(ifName)
    status = result.get_status()
    if(status.eq(STATUS.OK)):
        print ("Loopback interface '%s' config:" % ifName)
        response = result.get_data()
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print("\n")
    print ("<<< Show configuration of loopback interfaces on the '%s'"
           % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_loopback_interfaces_cfg()
    status = result.get_status()
    if(status.eq(STATUS.OK)):
        print "Loopback interfaces config:"
        lbIfCfg = result.get_data()
        print json.dumps(lbIfCfg, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print("\n")
    print ("<<< Show interfaces configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_interfaces_cfg()
    status = result.get_status()
    if(status.eq(STATUS.OK)):
        print "Interfaces config:"
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
        print ("'%s' NETCONF node was successfully removed "
               "from the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief())
        exit(0)

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
