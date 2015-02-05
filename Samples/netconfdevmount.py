'''
Created on Feb 3, 2015

@author: sergei
'''

import cStringIO
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError

import pycurl
import json
import base64

class BaseClass:
    def __init__(self):
        self.based = 11111
#        self.a = a
#        self.b = b
    def __repr__(self):
        return "BaseClass()"
    def __str__(self):
        return "BaseClass to string representation"
    def f1(self):        
        return ('I am the Base class')
    
    
'''    
print("netconfmount sample python script")
b = BaseClass()
print("+++" + repr(b))
print("+++" + str(b))
print("+++" + b.f1())
'''

'''
url="http://172.22.18.245:8181/restconf/operational/opendaylight-inventory:nodes"
c = pycurl.Curl()
c.setopt(c.URL, url)
buf = cStringIO.StringIO()
c.setopt(c.WRITEFUNCTION, buf.write)
#c.setopt(pycurl.VERBOSE, 1)
#headers = { 'Authorization' : 'Basic %s' % base64.b64encode("admin:admin") }
#c.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
c.setopt(pycurl.USERNAME, "admin")
c.setopt(pycurl.PASSWORD, "admin")
c.perform()

http_code = c.getinfo(pycurl.HTTP_CODE)
if http_code is 200:
    jsonData = json.loads(buf.getvalue().decode('utf-8'))    
#    jsonData = buf.getvalue()
    print jsonData   
#print jsonData

buf.close()
c.close
'''

#================================
def get_node_conf_status(ipAddr, portNum, uname, passwd, nodeId):
    url="http://" + ipAddr + ":" + portNum + "/restconf/config/opendaylight-inventory:nodes"
    status = "Node is not configured"
    
    try:
        resp = requests.get(url, auth=HTTPBasicAuth(uname, passwd))    
    except ConnectionError:
        status = "HTTP server connection error"
        return status
    
    if (resp.status_code != 200):
        status = "HTTP request error %d" % resp.status_code
        return status
        
    data = resp.content    
    d = json.loads(data)
    nodes = d.get('nodes')
    nodes_list = nodes.get('node')
    for elem in nodes_list:
        if(elem['id'] == nodeId):
            status = "Node is configured"
            break
        
    return status
#================================

#================================
#def get_node_conn_status(data, nodeId):
def get_node_conn_status(url, uname, passwd, nodeId):
    status = "Node is not connected"
    matchFound = False
    
    try:
        resp = requests.get(url, auth=HTTPBasicAuth(uname, passwd))    
    except ConnectionError:
        status = "HTTP server connection error"
        return status
    
    if (resp.status_code != 200):
        status = "HTTP request error %d" % resp.status_code
#        print resp.content
        return status

    # handle the exception    
#    print ("response status: %d" % resp.status_code)
#    print ("response headers: %s" % resp.headers['content-type'])
#    print ("response content: %s" % resp.content)
    
    
    data = resp.content
    
    d = json.loads(data)
#    print type(d)
    nodes = d.get('nodes')
#    print nodes
    nodes_list = nodes.get('node')
#    print node
#    print type(node)
#    print len(node)
    for elem in nodes_list:
#        print type(elem)
#        print elem
        if(elem['id'] == nodeId):
#            print "found match " + elem['id']
            if 'netconf-node-inventory:connected' in elem:
#                print "status is in elem"
#                print elem['netconf-node-inventory:connected']
#                print type(elem['netconf-node-inventory:connected'])
                if (elem['netconf-node-inventory:connected'] == True):
                    matchFound = True
                    status = "Node is connected"
                    break
#            else:
 #               print "status is not in elem"
                
            
#            if(elem['netconf-node-inventory:connected'])
        '''
#        print item['id']
#        print item['netconf-node-inventory:connected']
        for key in item.keys():
            print key
            if (item[key] == id):
                print "!!!"
                print item[key]
                status = "connected"
       '''
                
    if(matchFound == False):
        status = "Node is not found"
        
    return status
#================================



#================================
'''
def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, [key] + pre):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, [key] + pre):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield indict
'''

'''
print ("----------------------------------")
url="http://172.22.18.246:8181/restconf/operational/opendaylight-inventory:nodes"
resp = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'))
print ("response status: %d" % resp.status_code)
print ("response headers: %s" % resp.headers['content-type'])
print ("response content: %s" % resp.content)

data = resp.content
print data
print type(data)
#for item in data .items():
#    print item

d = json.loads(data)
print type(d)
nodes = d.get('nodes')
print nodes

node = nodes.get('node')
print node
print type(node)

print len(node)
for item in node:
#        print item
        print type(item)
#        print item['id']
#        print item['netconf-node-inventory:connected']
        for key in item.keys():
            print key
'''
bvcIpAddr =  "172.22.18.245"
bvcPortNum = "8181"     
bvcUname = 'admin' 
bvcPswd = 'admin'
nodeName = 'vRouter1'

print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
#conn_status = get_node_conn_status(resp.content, 'vRouter1')
url1="http://172.22.18.245:8181/restconf/operational/opendaylight-inventory:nodes"
conn_status = get_node_conn_status(url1, 'admin',  'admin', 'vRouter1')
print conn_status

print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
url2="http://172.22.18.245:8181/restconf/config/opendaylight-inventory:nodes"
#conf_status = get_node_conf_status(url2, 'admin',  'admin', 'vRouter1')
conf_status = get_node_conf_status(bvcIpAddr, bvcPortNum, bvcUname,  bvcPswd, nodeName)
print conf_status

#item = i.next() # fetch first value
#item = i.next() # fetch second value        
        
        
        

'''
a = iter(node)
for i in a:
    print(i)
    next(a)
'''



#print type(nodes)
#for key in nodes.keys():
#    print nodes[key]
#    print type(key)





#print obj
#for item in obj.items():
#    print type(item)

#data = resp.json()
#print data
#json_encoded = json.dumps(data)
#print json_encoded
#content = json.dumps(resp.content.decode('ASCII'))
#print content


'''
url="http://172.22.18.245:8181/restconf/operational/opendaylight-inventory:nodes"
#payload = {'inUserName': 'admin', 'inUserPass': 'admin'}
payload = {'inUserName': 'admin', 'inUserPass': 'admin'}

resp = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'))
#resp = requests.get(url, headers={'Authorization: Basic admin:admin'})
#resp = requests.get(url, data=payload)
print ("response status: %d" % resp.status_code)
print ("response headers: %s" % resp.headers['content-type'])
print ("response content: %s" % resp.content)

jsonData = json.loads(resp.content)
print "jsonData: %s" % jsonData
print ("+++++++++++++++++++++++++++++++++\n")
for obj in jsonData:
    print type(obj)
#    for item in obj.items():
#        print item

#for item in jsonData.items():
#    print item
'''
'''
for keys,values in json_obj.items():
    print(keys)
    print(values)
'''

#print resp.text
#string = resp.text
#json_obj = json.loads(string)
#print json_obj
#print json_obj.__getattribute__('nodes')




#print(json_obj['id'])
#print(resp.read()) 

#r = requests.get(url, data=payload)
#r = requests.get('http://www.example.com')
#print ("+++ r.status_code=%s" % r.status_code)
#print ("+++ r.status_code=%s" % r.  .status_code)


