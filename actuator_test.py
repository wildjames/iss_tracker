import itertools
import time
from time import sleep

from numpy.random import randint

from servo import Servo
from stepper import stepMotors

# Datasheet: https://www.bitsbox.co.uk/data/motor/sg90.pdf
min_pw = 1e-3
max_pw = 2e-3
frame  = 20e-3

servo = Servo(14)

stepper_pins = [17, 27, 22, 10] # Set the gpios being used here, in order
move = stepMotors(stepper_pins)

DELAY = 5 # seconds

stepper_angle = 0
try:
    while True:
        stepper_angle += 90
        print("Moving to {} deg".format(stepper_angle))
        move.to_angle(stepper_angle)
        servo.value = stepper_angle % 180

        time.sleep(DELAY)


        stepper_angle += 90
        print("Moving to {} deg".format(stepper_angle))
        move.to_angle(stepper_angle)
        servo.value = stepper_angle % 180

        time.sleep(DELAY)

except KeyboardInterrupt:
    servo.close()
