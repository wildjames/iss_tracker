import itertools
import time
from time import sleep

from gpiozero import Button, DigitalOutputDevice
from numpy.random import randint

from servo import Servo
from stepper import stepMotors

servo = Servo(13)

stepper_pins = [17, 27, 22, 10] # Set the gpios being used here, in order
switch_pin = 11
move = stepMotors(stepper_pins)

DELAY = 1 # seconds

# Test the homing of the stepper
switch_rail = DigitalOutputDevice(0)
switch = Button(switch_pin)

print("Homing the stepper motor...  ", end='')
move.home(switch)
print("Done!")

servo_angle = 0
stepper_angle = 0
try:
    while True:
        stepper_angle += 15
        servo_angle += 15
        if servo_angle >= servo.max_angle:
            servo_angle = servo.min_angle

        print("Moving to {} deg".format(stepper_angle))
        move.to_angle(stepper_angle, block=True)
        servo.angle = servo_angle

        time.sleep(DELAY)


        stepper_angle += 0
        servo_angle += 15
        if servo_angle >= servo.max_angle:
            servo_angle = servo.min_angle

        print("Moving to {} deg".format(stepper_angle))
        move.to_angle(stepper_angle)
        servo.angle = servo_angle

        time.sleep(DELAY)

except KeyboardInterrupt:
    servo.close()
    move.cleanup()
