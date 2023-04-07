#!/usr/bin/env python3
import requests
from dnac_config import *
from get_token import get_auth_token

def get_device_list():
    token = get_auth_token()
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type': 'application/json'}
    # prm = {'id': 'f0cb8464-1ce7-4afe-9c0d-a4b0cc5ee84c'}

    resp = requests.get(url, headers=hdr, verify=False)

    device_list = resp.json()

    print_device_list(device_list)


def print_device_list(device_json):
    print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
          format("hostname", "mgmt IP", "serial", "platformId", "SW Version", 'role', 'upTime'))
    
    for device in device_json['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if device['serialNumber'] is not None and ',' in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(','), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        
        for (serialNumber, platformId) in serialPlatformList:
            print("{0:42}{1:17}{2:12}{3:18}{4:12}{4:12}{5:16}{6:15}".
                  format(device['hostname'], device['managementIpAddress'],
                         serialNumber, platformId, device['softwareVersion'],
                         device['role'], uptime))


if __name__=='__main__':
    get_device_list()