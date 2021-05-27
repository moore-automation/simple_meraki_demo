import sys
import getopt
import requests
import json
import time
import meraki


def main():

    arg_apikey = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
    arg_orgname = 'DevNet Sandbox'
    arg_nwname = 'DevNet Sandbox ALWAYS ON'

    dashboard = meraki.DashboardAPI(arg_apikey)
    org_output = dashboard.organizations.getOrganizations()
    org_id = id_loop(org_output, arg_orgname)
    net_output = dashboard.organizations.getOrganizationNetworks(org_id)
    net_id = id_loop(net_output, arg_nwname)
    dev_output = dashboard.networks.getNetworkDevices(net_id)

    print("\n{0:25}{1:25}{2:25}{3:25}{4:25}".format(
        "Device Hostname", "LAN IP Address", "WAN IP Address", "Model", "Serial Number"))
    for device in dev_output:
        # this is really horrible but sometimes the name/ip's aren't set.
        name = device.get('name', "")
        wan = device.get('wan1Ip', "")
        lan = device.get('lanIp', " ")
        # if both wan and lan are empty meraki sets lanIp to none instead of '' 
        ip = str(wan)+str(lan) if lan != None else str(wan)

        print("{0:25}{1:25}{2:25}{3:25}".format(
            name, ip, device['model'], device['serial']))
    return('null')


def id_loop(list, value):
    for x in list:
        if x['name'] == value:
            return x['id']


if __name__ == '__main__':
    main()
