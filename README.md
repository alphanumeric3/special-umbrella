# ap-research

Counting certain APs around me using Kismet & its API.

Very simple for now, I just walk around with Kismet and check the API using collect.py.

This came from a conversation I had about how many WiFi access points my college has!

Other methods I could try:
- Using NetworkManager, grep, uniq and other small tools to build a list. But Kismet offers
more info which I could use in the future
- Using Kismet's wardriving override, it outputs to a CSV (.wiglecsv) so it's convenient to
parse. This takes the script I made out of the equation, because it doesn't work in wardriving mode.
