import datetime
import json
import urllib.request
from time import sleep

import geocoder
from gpiozero import Button, DigitalOutputDevice, PWMLED
from orbit_predictor import locations
from orbit_predictor.coordinate_systems import ecef_to_llh
from orbit_predictor.sources import get_predictor_from_tle_lines

import Adafruit_CharLCD as LCD
from servo import Servo
from stepper import stepMotors


def get_satlist():
    url = "https://www.celestrak.com/NORAD/elements/stations.txt"
    response = urllib.request.urlopen(url)

    content = [line.decode('ascii') for line in response.readlines()]

    station_names = [name.strip() for name in content[::3]]
    satlist = []
    i = 0
    while i < len(content):
        lines = [content[i+1], content[i+2]]
        satlist.append(lines)
        i += 3

    return station_names, satlist

def get_satellite(index, station_names, satlist):
    line1, line2 = satlist[index]
    TLE_LINES = (line1, line2)
    predictor = get_predictor_from_tle_lines(TLE_LINES)

    lcd.set_cursor(0,0)
    lcd.message("{:<16s}".format(station_names[index]))

    return predictor, station_names[index]

# I should do this with a class and an iterator rather than a global call, but fuck it
def cycle_station():
    global current_index
    global station_names
    global satlist
    global tracking
    global predictor
    global lcd

    current_index += 1
    current_index = current_index % len(station_names)

    # Set the stuff
    predictor, tracking = get_satellite(current_index, station_names, satlist)

def revert_ISS():
    global station_names
    global satlist
    global current_index

    current_index = 0
    # Set the stuff
    predictor, tracking = get_satellite(current_index, station_names, satlist)


if __name__ in "__main__":
    # Set the gpios being used here
    stepper_pins = [3, 4, 14, 15]
    servo_pin = 2

    homeswitch_pin = 17

    cycle_button_pin = 25

    # LCD pins
    lcd_rs = 27
    lcd_en = 22
    lcd_backlight_pin = 18

    lcd_d4 = 23
    lcd_d5 = 24
    lcd_d6 = 10
    lcd_d7 = 9

    lcd_columns = 16
    lcd_rows = 2


    # Time between updates, sec
    DELAY = 1

    lcd = LCD.Adafruit_CharLCD(
        lcd_rs, lcd_en,
        lcd_d4, lcd_d5, lcd_d6, lcd_d7,
        lcd_columns, lcd_rows
    )
    lcd_backlight = PWMLED(lcd_backlight_pin, initial_value=1.0)

    lcd.message("FETCHING SAT.\nLIST...")

    try:
        station_names, satlist = get_satlist()
        current_index = 0
        last_update = datetime.datetime.utcnow()
    except urllib.error.URLError:
        lcd.message("FAILED TO GET STATION LIST")
        while True:
            try:
                station_names, satlist = get_satlist()
                current_index = 0
                last_update = datetime.datetime.utcnow()
            except urllib.error.URLError:
                lcd.message("FAILED TO GET STATION LIST")
                sleep(30)

    # Where am I? Fetch from IP location.
    g = geocoder.ip('me')
    lat, lon = g.latlng
    me = locations.Location('me', lat, lon, 0)

    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.message("I am at lat, lon\n{:<8.2f}{:>8.2f}".format(lat, lon))
    sleep(10)

    # Set up actuators
    elevation_actuator = Servo(
        servo_pin,
        initial_angle=0, min_angle=-101, max_angle=84,
        min_allowed=-90)
    azimuth_actuator = stepMotors(stepper_pins)

    # Buttons
    switch = Button(homeswitch_pin)
    cycle_button = Button(
        cycle_button_pin,
        bounce_time=0.01,
        hold_time=5.0,
    )
    cycle_button.when_pressed = cycle_station
    cycle_button.when_held = revert_ISS


    # Home the stepper
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.message("Homing\nstepper motor...  ")

    azimuth_actuator.home(switch)

    lcd.clear()
    predictor, tracking = get_satellite(current_index, station_names, satlist)

    # Main loop
    time = datetime.datetime.utcnow()
    dt = datetime.timedelta(minutes=1)
    try:
        while True:

            time = datetime.datetime.utcnow()
            # The positions are returned in Earth-centric, Earth fixed coords. I need to convert those.
            ecef_location = locations.Location('station', *ecef_to_llh(predictor.get_only_position(time)))

            ### Convert ECEF to alt, az ###
            az, elev = me.get_azimuth_elev_deg(ecef_location)

            lcd.set_cursor(0,1)
            lcd.message("{:<8.2f}{:>8.2f}".format(az, elev))

            # Move the actuators to the right angles
            elevation_actuator.angle = elev
            azimuth_actuator.to_angle(az, block=True)

            stop = time + datetime.timedelta(seconds=DELAY)
            while datetime.datetime.utcnow() < stop:
                sleep(0.1)

            next_update = time + datetime.timedelta(days=1)
            if next_update < last_update:
                try:
                    predictor, tracking = get_satellite(current_index, station_names, satlist)
                    last_update = datetime.datetime.utcnow()
                except:
                    pass

    except:
        azimuth_actuator.to_angle(0.0)
        elevation_actuator.angle = -90.0

        azimuth_actuator.cleanup()
        elevation_actuator.close()
        lcd.clear()
        lcd.set_cursor(0,0)
        lcd.message("Fine, leave,\nsee if I care")

