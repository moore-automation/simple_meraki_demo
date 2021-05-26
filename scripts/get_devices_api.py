import sys
import getopt
import requests
import json
import time


def main():

    # Enter API_Key
    arg_apikey = ''
    arg_orgname = ''
    arg_nwname = ''
    arg_url = 'api.meraki.com'

    org_id = getorgid(arg_apikey, arg_orgname)
    nw_id = getnwid(arg_apikey, arg_url, org_id, arg_nwname)
    getalldevid(arg_apikey, arg_url, nw_id)


def getorgid(p_apikey, p_orgname):
    # looks up org id for a specific org name
    # on failure returns 'null'
    try:
        r = requests.get('https://dashboard.meraki.com/api/v1/organizations', headers={
                         'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
    except:
        print('ERROR 00: Unable to contact Meraki cloud')
        sys.exit(2)

    if r.status_code != requests.codes.ok:
        return 'null'

    rjson = r.json()

    for record in rjson:
        if record['name'] == p_orgname:
            print("\nOrganisation ({0}) has an Organisation ID : {1}".format(
                p_orgname, record['id']))
            return record['id']

    return('null')


def getnwid(p_apikey, p_shardurl, p_orgid, p_nwname):
    # looks up network id for a network name
    # on failure returns 'null'

    try:
        r = requests.get('https://%s/api/v1/organizations/%s/networks' % (p_shardurl, p_orgid),
                         headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
    except:
        print('ERROR 02: Unable to contact Meraki cloud')
        sys.exit(2)

    if r.status_code != requests.codes.ok:
        return 'null'

    rjson = r.json()

    for record in rjson:
        if record['name'] == p_nwname:
            print("\nNetwork ({0}) has an Network ID : {1}".format(
                p_nwname, record['id']))
            return record['id']
    return('null')


def getalldevid(p_apikey, p_shardurl, p_networkid):

    try:
        r = requests.get('https://%s/api/v1/networks/%s/devices' % (p_shardurl, p_networkid),
                         headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
    except:
        print('ERROR 02: Unable to contact Meraki cloud')
        sys.exit(2)

    if r.status_code != requests.codes.ok:
        return 'null'

    rjson = r.json()
    print("\n{0:25}{1:25}{2:25}{3:25}".format(
        "Device Hostname", "IP Address", "Model", "Serial Number"))
    for device in rjson:
        if 'wan1Ip' in device:
            print("{0:25}{1:25}{2:25}{3:25}".format(
                device['name'], device['wan1Ip'], device['model'], device['serial']))
        else:
            print("{0:25}{1:25}{2:25}{3:25}".format(
                device['name'], device['lanIp'], device['model'],device['serial']))
    return('null')


if __name__ == '__main__':
    main()
