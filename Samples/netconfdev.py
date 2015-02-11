'''
Created on Feb 3, 2015

@author: sergei
'''

#import requests
#from requests.auth import HTTPBasicAuth
#from requests.exceptions import ConnectionError
#import pprint
#import xmltodict
#import json

#================================
# KEEP
#================================
class NetconfDevice(object):
    def __init__(self, devName, ipAddr, portNum, tcpOnly, adminName, adminPassword):
        self.devName = devName
        self.ipAddr = ipAddr
        self.tcpOnly = tcpOnly
        self.portNum = portNum
        self.adminName = adminName
        self.adminPassword = adminPassword

    def to_string(self):
        return str(vars(self))

 
