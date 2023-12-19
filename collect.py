#!/usr/bin/python3
import requests
import json
import sys

kismet_url = "http://localhost:2501"
username = sys.argv[1]
password = sys.argv[2] # !!!: USE A TOKEN INSTEAD! ARGHHH!!!
search_query = sys.argv[3]
auth = (username, password)

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
    "search": search_query,
    "json": json.dumps(json_param)
}

# this endpoint returns seen SSIDs
ssids = requests.post(
    f"{kismet_url}/phy/phy80211/ssids/views/ssids.json",
    auth=auth,
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
        ["kismet.device.base.crypt", "crypt"]
    ]
}
access_points = requests.post(
    f"{kismet_url}/devices/multikey/devices.json",
    auth=auth,
    json=body
).json()

for ap in access_points:
    print(f"{ap['clients']} | {ap['macaddr']} | {ap['manuf']} | {ap['crypt']}")
