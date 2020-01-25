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

def get_satlist():
    url = "https://www.celestrak.com/NORAD/elements/stations.txt"
    response = urllib.request.urlopen(url)

    content = [line.decode('ascii') for line in response.readlines()]

    station_names = content[::3]
    satlist = []
    i = 0
    while i < len(content)
        lines = [content[i+1], content[i+2]]
        satlist.append(lines)
        i += 3

    return station_names, satlist

def get_satellite(index, station_names, satlist):
    line1, line2 = satlist[index]
    TLE_LINES = (line1, line2)
    predictor = get_predictor_from_tle_lines(TLE_LINES)

    return predictor, station_names[index]

# I should do this with a class and an iterator rather than a global call, but fuck it
def cycle_station():
    global current_index
    global station_names
    global tracking
    global predictor

    current_index += 1
    current_index = current_index % len(station_names)

    # Set the stuff
    tracking = station_names.next()
    print("\n\n  Tracking {}".format(tracking))
    predictor = get_satellite(current_index)


if __name__ in "__main__":
    # Set the gpios being used here, in order
    stepper_pins = [17, 27, 22, 10]
    servo_pin = 13
    rail_pin = 0
    switch_pin = 11
    cycle_button_pin = 12

    station_names, satlist = get_satlist()
    current_index = 0

    print("Getting first predictor...  ", end='')
    predictor, tracking = get_satellite(current_index, satlist)
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
    cycle_button = Button(
        cycle_button_pin,
        bounce_time=0.01
    )
    cycle_button.when_pressed = cycle_station
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
            print("  {} alt, elev at {}: {:6.2f}, {:6.2f}".format(tracking, timestr, az, elev), end='\r')

            # Move the actuators to the right angles
            elevation_actuator.angle = elev
            azimuth_actuator.to_angle(az, block=True)

            stop = time + datetime.timedelta(seconds=DELAY)
            while datetime.datetime.utcnow() < stop:
                sleep(0.1)

            next_update = time + datetime.timedelta(days=1)
            if next_update < last_update:
                try:
                    timestr = time.strftime("%Y, %d, %m at %H:%M")
                    print("\nUpdating predictor for {} (time is {})...  ".format(tracking, timestr), end='')
                    predictor, tracking = get_satellite(current_index, satlist)
                    last_update = datetime.datetime.utcnow()
                    print("Done!")
                except:
                    pass

    except:
        azimuth_actuator.close()
        elevation_actuator.close()