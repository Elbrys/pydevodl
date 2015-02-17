import json

class NetconfNode(object):
    def __init__(self, controller=None, nodeName=None, ipAddr=None, portNum=None,
                 adminName=None, adminPassword=None, tcpOnly=False):
        self.ctrl = controller
        self.name = nodeName
        self.ipAddr = ipAddr
        self.tcpOnly = tcpOnly
        self.portNum = portNum
        self.adminName = adminName
        self.adminPassword = adminPassword

    def to_string(self):
        return str(vars(self))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
