import sys
import getopt
import requests
import json
import time
import meraki


def main():

    arg_apikey = ''

    dashboard = meraki.DashboardAPI(arg_apikey)
    org_output = dashboard.organizations.getOrganizations()
    org_id = org_output[0]['id']
    net_output = dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')
    net_id = net_output[0]['id']
    dev_output = dashboard.networks.getNetworkDevices(net_id)

    print("\n{0:25}{1:25}{2:25}{3:25}{4:25}".format(
        "Device Hostname", "LAN IP Address", "WAN IP Address", "Model", "Serial Number"))
    for device in dev_output:
        if 'wan1Ip' in device:
            print("{0:25}{1:25}{2:25}{3:25}{4:25}".format(
                device['name'], str(device['wan1Ip']), str(device['lanIp']), device['model'], device['serial']))
        else:
            print("{0:25}{1:25}{2:25}{3:25}".format(
                device['name'], device['lanIp'], device['model'], device['serial']))


if __name__ == '__main__':
    main()
