import urllib.request
import json
import time

from pprint import pprint


# https://wheretheiss.at/w/developer
url = "https://api.wheretheiss.at/v1/satellites/25544"
response = urllib.request.urlopen(url)
result = json.loads(response.read())

# Request the ISS location.
lat = float(result["latitude"])
lon = float(result["longitude"])
alt = float(result['altitude'])

pprint(result)

print("\n\n\nISS lat, lon, alt: {:.4f}, {:.4f}, {:.4f} km".format(lat, lon, alt))
# This must be converted to an alt, az.
# TODO: Copy code from my TLE_sats.py script?

