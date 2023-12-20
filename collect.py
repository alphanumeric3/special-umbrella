#!/usr/bin/python3
import requests
import json
import sys

kismet_url = "http://localhost:2501"
token = sys.argv[1]
search_query = sys.argv[2]

# only select specific fields
json_param = {
    "fields": [
        "dot11.ssidgroup.ssid",
        # maybe i could take a diff of these two
        "dot11.ssidgroup.responding_devices",
        "dot11.ssidgroup.advertising_devices"
    ]
}

# currently, the search thing doesn't work
params = {
    "KISMET": token,
    "search": search_query,
    "json": json.dumps(json_param)
}

# this endpoint returns seen SSIDs
ssids = requests.post(
    f"{kismet_url}/phy/phy80211/ssids/views/ssids.json",
    params=params
).json()

# TODO: i need to make the search thing in the above request actually work,
# then i won't need to do this. or maybe i am using the wrong endpoint.
# filter for the SSID (search_query)
network = None
for result in ssids:
    if result['dot11.ssidgroup.ssid'] == search_query:
        network = result
        break
if network == None:
    print(f"couldn't find {search_query}, quitting")
    sys.exit(1)

# if successful, check the responding devices
body = {
    "devices": network['dot11.ssidgroup.responding_devices'],
    "fields": [
        ["kismet.device.base.manuf", "manuf"],
        ["kismet.device.base.macaddr", "macaddr"],
        ["dot11.device/dot11.device.num_associated_clients", "clients"],
        ["kismet.device.base.crypt", "crypt"],
        ["kismet.device.base.signal/kismet.common.signal.last_signal", "last_signal"] # unit is dbm
    ]
}
access_points = requests.post(
    f"{kismet_url}/devices/multikey/devices.json",
    params={"KISMET": token},
    json=body
).json()

# print(network['dot11.ssidgroup.responding_devices'])
print("APs found:", len(access_points))
total_clients = sum([ap['clients'] for ap in access_points])
print("Total clients:", total_clients)
for ap in access_points:
    print(f"{ap['clients']} | {ap['last_signal']} | {ap['macaddr']} | {ap['manuf']} | {ap['crypt']}")
