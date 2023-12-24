# ap-research

Repo for when I walked around counting WiFi APs for an SSID.

It's very simple for now, I just walk around with Kismet running, and query the BSSID/MAC,
SSID and manufacturer.

This came from a conversation I had about how many access points a building has!

## How to use

1. Run Kismet. You can use the (hopefully) included wardriving config with
`kismet --override wardrive -T kismet` to only collect WiFi networks, and not
devices connected.

2. Then run `./query.sh <name of db> <ssid to look for>`. The name of
the database is the newly created `.kismet` file.  
I like running this with `watch -n 0.5 -d ./query.sh <db> <ssid>`.

## collect.py

collect.py is a previous method for this. It uses Kismet's API instead, and shows
the amount of associated devices per AP (doesn't work in wardriving mode).
