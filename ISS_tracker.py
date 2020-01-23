import datetime
import json
import urllib.request
from time import sleep

import geocoder
from orbit_predictor import locations
from orbit_predictor.coordinate_systems import ecef_to_llh
from orbit_predictor.sources import get_predictor_from_tle_lines

from servo import Servo
from stepper import stepMotors

g = geocoder.ip('me')
lat, lon = g.latlng
me = locations.Location('me', lat, lon, 0)

url = "https://www.celestrak.com/NORAD/elements/stations.txt"
response = urllib.request.urlopen(url)

content = [line.decode('ascii') for line in response.readlines()]

for i, line in enumerate(content):
    print(line)
    if 'ISS (ZARYA)' in line:
        line1 = content[i+1]
        line2 = content[i+2]
        break

TLE_LINES = (line1, line2)
predictor = get_predictor_from_tle_lines(TLE_LINES)

print("\n\n\nI am at lat, long: {:.3f}, {:.3f}\n".format(lat, lon))

print("Setting up the actuators...")

elevation_actuator = Servo(13, 0, -90, 90)

stepper_pins = [17, 27, 22, 10] # Set the gpios being used here, in order
azimuth_actuator = stepMotors(stepper_pins)

DELAY = 5 # seconds


while True:
    # The positions are returned in Earth-centric, Earth fixed coords. I need to convert those.
    now = datetime.datetime.utcnow()
    ecef_location = locations.Location('ISS', *ecef_to_llh(predictor.get_only_position(now)))

    ### Convert ECEF to alt, az ###
    az, elev = me.get_azimuth_elev_deg(ecef_location)

    print("  ISS alt, elev: {:6.2f}, {:6.2f}".format(az, elev), end='\r')

    elevation_actuator.angle = elev
    azimuth_actuator.to_angle(az)

    sleep(DELAY)
