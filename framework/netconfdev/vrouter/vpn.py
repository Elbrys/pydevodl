"""
Copyright (c) 2015

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 - Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
-  Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
-  Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES;LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@authors: Sergei Garbuzov
@status: Development
@version: 1.1.0

vpn.py: Virtual Private Network (VPN) specific properties and access methods


"""
import json

from framework.common.utils import strip_none, remove_empty_from_dict, dict_keys_underscored_to_dashed

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Vpn():
    ''' Class representing Virtual Private Network (VPN) configuration '''
    
    _mn1 = "vyatta-security:security"
    _mn2 = "vyatta-security-vpn-ipsec:vpn"
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.ipsec = Ipsec()
        self.l2tp = L2tp()
        self.rsa_keys = RsaKeys()
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def get_payload(self):
        s = self.to_json()
        obj = json.loads(s)
        obj1 = strip_none(obj)
        obj2 = remove_empty_from_dict(obj1)
        obj3 = dict_keys_underscored_to_dashed(obj2)
        payload = {self._mn1:{self._mn2:obj3}}
        return json.dumps(payload, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ipsec(self, ipsec):
        if ipsec != None and isinstance(ipsec, Ipsec):
            self.ipsec = ipsec
        else:
            raise TypeError("")
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp(self, l2tp):
        if l2tp != None and isinstance(l2tp, L2tp):
            self.l2tp = l2tp
        else:
            raise TypeError("")
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_rsa_keys(self, rsa_keys):
        if rsa_keys != None and isinstance(rsa_keys, RsaKeys):
            self.rsa_keys = rsa_keys
        else:
            raise TypeError("")
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_local_key(self, path):
        if isinstance(path, basestring):
            self.rsa_keys.set_local_key(path)
        else:
            raise TypeError("")
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_rsa_key(self, name, value):
        if (isinstance(name, basestring) and isinstance(value, basestring)):
            self.rsa_keys.set_rsa_key(name, value)
        else:
            raise TypeError("")
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_nat_traversal(self, value):
        if (isinstance(value, bool)):
            self.ipsec.set_nat_traversal(value)
        else:
            raise TypeError("")
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_nat_allow_network(self, ipnet):
        self.ipsec.set_nat_allow_network(ipnet)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_user_auth_mode(self, mode):
        self.l2tp.remote_access.set_auth_mode(mode)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_user(self, name, pswd):
        self.l2tp.remote_access.set_local_user(name, pswd)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_ipsec_auth(self, mode, secret):
        self.l2tp.remote_access.set_ipsec_mode(mode)
        self.l2tp.remote_access.set_ipsec_pre_shared_secret(secret)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_client_ip_pool(self, start, end):
        self.l2tp.remote_access.set_client_ip_pool(start, end)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_outside_address(self, ipaddr):
        self.l2tp.remote_access.set_outside_address(ipaddr)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_outside_nexthop(self, ipaddr):
        self.l2tp.remote_access.set_outside_nexthop(ipaddr)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_description(self, description):
        self.l2tp.remote_access.set_description(description)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_server_ip_pool(self, start, end):
        self.l2tp.remote_access.set_server_ip_pool(start, end)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_dhcp_interface(self, interface):
        self.l2tp.remote_access.set_dhcp_interface(interface)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_primary_dns_server(self, ipaddr):
        self.l2tp.remote_access.set_primary_dns_server(ipaddr)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_secondary_dns_server(self, ipaddr):
        self.l2tp.remote_access.set_secondary_dns_server(ipaddr)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_primary_wins_server(self, ipaddr):
        self.l2tp.remote_access.set_primary_wins_server(ipaddr)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_secondary_wins_server(self, ipaddr):
        self.l2tp.remote_access.set_secondary_wins_server(ipaddr)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_l2tp_remote_access_mtu(self, mtu):
        self.l2tp.remote_access.set_mtu(mtu)

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Ipsec(Vpn):
    ''' Class representing VPN IP security (IPsec) configuration
        Helper class of the 'Vpn' class '''
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        
        ''' Auto update interval for IPsec daemon (must be between 30 and 65535) '''
        self.auto_update = None
        
        ''' Option to disable requirement for unique IDs in the Security Database '''
        self.disable_uniqreqids = None
        
        ''' Encapsulating Security Payload (ESP) groups
            (list of 'EspGroup' class instances) '''
        self.esp_group = []
        
        ''' Internet Key Exchange (IKE) groups 
            (list of 'IkeGroup' class instances) '''
        self.ike_group = []
        
        ''' IPsec logging 
           'enumeration: raw', 'crypt', 'parsing', 'emitting', 'control', 'private', 'all' '''
        self.logging = None
        
        ''' Network Address Translation (NAT) networks '''
        self.nat_networks = None
        
        ''' Network Address Translation (NAT) traversal
           enumeration: 'enable', 'disable' '''
        self.nat_traversal = None
        
        ''' VPN IPSec Profiles
            (list of IpSecProfile class instances) '''
        self.profile = []
        
        ''' Site to site VPN 
            (instance of 'SiteToSite' class)'''
        self.site_to_site = None
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_auto_update(self, interval):
        self.auto_update = interval
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_disable_uniqreqids(self):
        self.disable_uniqreqids = ""
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_nat_traversal(self, value):
        assert(isinstance(value, bool))
        self.nat_traversal = "enable" if (value) else "disable"
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_nat_allow_network(self, ipnet):
        if (self.nat_networks == None):
            self.nat_networks = {'allowed_network': []}
        d = {'tagnode' : ipnet}
        self.nat_networks['allowed_network'].append(d)

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class L2tp(Vpn):    
    ''' Class representing VPN Layer 2 Tunneling Protocol (L2TP) configuration
        Helper class of the 'Vpn' class '''
    
    def __init__(self):
        self.remote_access = RemoteAccess()

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class RemoteAccess(L2tp):
    ''' Helper class of the 'L2tp' class '''
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.authentication = Authentication()
        self.client_ip_pool = None
        self.description = None
        self.dhcp_interface = None
        self.dns_servers = {'server_1' : None, 'server_2' : None}
        self.ipsec_settings = IpSecSettings()
        self.mtu = None
        self.outside_address = None
        self.outside_nexthop = None
        self.server_ip_pool = None
        self.wins_servers = {'server_1' : None, 'server_2' : None}
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_auth_mode(self, mode):
        self.authentication.set_mode(mode)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_local_user(self, name, pswd):
        self.authentication.set_user(name, pswd)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ipsec_mode(self, mode):
        self.ipsec_settings.set_mode(mode)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_ipsec_pre_shared_secret(self,secret):
        self.ipsec_settings.set_secret(secret)
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_client_ip_pool(self, start, end):
        self.client_ip_pool = {'start' : start, 'stop' : end}
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_outside_address(self, ipaddr):
        self.outside_address = ipaddr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_outside_nexthop(self, ipaddr):
        self.outside_nexthop = ipaddr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_description(self, description):
        self.description = description
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_server_ip_pool(self, start, end):
        self.server_ip_pool = {'start' : start, 'stop' : end}
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_dhcp_interface(self, interface):
        self.dhcp_interface = interface
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_primary_dns_server(self, ipaddr):
        self.dns_servers['server_1'] = ipaddr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_secondary_dns_server(self, ipaddr):
        self.dns_servers['server_2'] = ipaddr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_primary_wins_server(self, ipaddr):
        self.wins_servers['server_1'] = ipaddr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_secondary_wins_server(self, ipaddr):
        self.wins_servers['server_2'] = ipaddr
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_mtu(self, mtu):
        self.mtu = mtu

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class Authentication(RemoteAccess):
    ''' Helper class of the 'RemoteAccess' class '''
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.local_users = {'username' : []}
        self.mode = None
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_mode(self, mode):
        self.mode = mode
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_user(self, name, pswd):
        d = {'tagnode' : name, 'password' : pswd}
        self.local_users['username'].append(d)

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class IpSecSettings(RemoteAccess):
    ''' Helper class of the 'RemoteAccess' class '''
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.authentication = {'mode': None, 'pre_shared_secret' : None}
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_mode(self, mode):
        self.authentication['mode'] = mode
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_secret(self, secret):
        self.authentication['pre_shared_secret'] = secret

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
class RsaKeys(Vpn):
    ''' Class representing VPN RSA keys configuration 
        Helper class of the 'Vpn' class '''
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def __init__(self):
        self.local_key = {'file': None}
        self.rsa_key_name = []
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_local_key(self, path):
        self.local_key['file'] = path
    
    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def set_rsa_key(self, name, value):
        d = {'rsa_key' : value, 'tagnode' : name}
        self.rsa_key_name.append(d)
