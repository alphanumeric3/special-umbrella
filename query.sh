#!/bin/bash
if [ -z "$1" ] || [ -z "$2" ]; then
	echo "usage: $0 [kismet database] [ssid]"
	exit 1
fi
# note: if 'box' output is causing you trouble, try 'table' instead
sqlite3 "$1" << EOF
select
	"APs found: " || count(device)
from devices where json_extract(device,'$."kismet.device.base.name"') like "$2";
.mode box
select 
	json_extract(device,'$."kismet.device.base.name"') as ssid,
	json_extract(device,'$."kismet.device.base.macaddr"') as mac,
	json_extract(device,'$."kismet.device.base.manuf"') as manuf
from devices where SSID like "$2";
EOF
