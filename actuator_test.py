from gpiozero import Servo, OutputDevice
from time import sleep
from stepper import stepMotors
import pigpio
import itertools
import time
from numpy.random import randint


servo = Servo(14)

stepper_pins = [17, 27, 22, 10] # Set the gpios being used here, in order
move = stepMotors(stepper_pins)

DELAY = 5 # seconds

stepper_angle = 0
while True:
    stepper_angle += 90
    print("Moving to {} deg".format(stepper_angle))
    move.to_angle(stepper_angle)
    servo.min()
    time.sleep(DELAY)

    stepper_angle += 90
    print("Moving to {} deg".format(stepper_angle))
    move.to_angle(stepper_angle)
    servo.max()
    time.sleep(DELAY)


