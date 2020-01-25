import datetime
import json
import urllib.request
from time import sleep

import geocoder
from orbit_predictor import locations
from orbit_predictor.coordinate_systems import ecef_to_llh
from orbit_predictor.sources import get_predictor_from_tle_lines

from gpiozero import DigitalOutputDevice, Button
from servo import Servo
from stepper import stepMotors

def get_satellite(satname='ISS (ZARYA)'):
    url = "https://www.celestrak.com/NORAD/elements/stations.txt"
    response = urllib.request.urlopen(url)

    content = [line.decode('ascii') for line in response.readlines()]

    for i, line in enumerate(content):
        print(line)
        if satname in line:
            line1 = content[i+1]
            line2 = content[i+2]
            break

    TLE_LINES = (line1, line2)
    predictor = get_predictor_from_tle_lines(TLE_LINES)

    return predictor

# I should do this with a class and an iterator rather than a global call, but fuck it
def cycle_station():
    global station_names
    global tracking
    global predictor

    current_index = station_names.index(tracking)
    current_index += 1
    current_index = current_index % len(station_names)

    # Set the stuff
    tracking = station_names[current_index]
    predictor = get_satellite(tracking)


if __name__ in "__main__":
    stepper_pins = [17, 27, 22, 10] # Set the gpios being used here, in order
    servo_pin = 13
    rail_pin
    switch_pin = 11
    cycle_button_pin = 12

    # Get a list of stations
    url = "https://www.celestrak.com/NORAD/elements/stations.txt"
    response = urllib.request.urlopen(url)
    content = [line.decode('ascii') for line in response.readlines()]
    station_names = content[::3]

    # Start with the ISS
    tracking = station_names[0]
    for station in station_names:
        if "ISS (ZARYA)" in station:
            tracking = station

    print("Getting predictor for the ISS...  ", end='')
    predictor = get_satellite(tracking)
    last_update = datetime.datetime.utcnow()
    print("Done!")

    g = geocoder.ip('me')
    lat, lon = g.latlng
    me = locations.Location('me', lat, lon, 0)


    print("Setting up the actuators...  ", end='')
    elevation_actuator = Servo(servo_pin, 0, min_angle=-87, max_angle=108, min_allowed=-45)
    azimuth_actuator = stepMotors(stepper_pins)
    print("Done!")

    # Test the homing of the stepper
    switch_rail = DigitalOutputDevice(rail_pin)
    switch_rail.on()
    switch = Button(switch_pin)

    print("Homing the stepper motor...  ", end='')
    azimuth_actuator.home(switch)
    print("Done!")

    print("Setting up the cycler pin...  ", end='')
    cycle_button = Button(cycle_button_pin)
    cycle_button.when_activated(cycle_station)
    print("Done!")


    # Refresh rate, sec
    DELAY = 1

    print("\nI am at lat, long: {:.3f}, {:.3f}\n".format(lat, lon))
    time = datetime.datetime.utcnow()
    dt = datetime.timedelta(minutes=1)
    try:
        while True:

            time = datetime.datetime.utcnow()
            # The positions are returned in Earth-centric, Earth fixed coords. I need to convert those.
            ecef_location = locations.Location('', *ecef_to_llh(predictor.get_only_position(time)))

            ### Convert ECEF to alt, az ###
            az, elev = me.get_azimuth_elev_deg(ecef_location)

            timestr = time.strftime("%H:%M")
            print("  ISS alt, elev at {}: {:6.2f}, {:6.2f}".format(timestr, az, elev), end='\r')

            # Move the actuators to the right angles
            elevation_actuator.angle = elev
            azimuth_actuator.to_angle(az, block=True)

            stop = time + datetime.timedelta(seconds=DELAY)
            while datetime.datetime.utcnow() < stop:
                sleep(0.1)

            next_update = time + datetime.timedelta(days=1)
            if next_update < last_update:
                timestr = time.strftime("%Y, %d, %m at %H:%M")
                print("\nUpdating predictor for {} (time is {})...  ".format(tracking, timestr), end='')
                predictor = get_satellite(tracking)
                last_update = datetime.datetime.utcnow()
                print("Done!")

    except:
        azimuth_actuator.close()
        elevation_actuator.close()