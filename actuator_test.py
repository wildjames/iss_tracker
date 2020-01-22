from gpiozero import Servo, OutputDevice
from time import sleep
from stepper import stepMotors
import pigpio
import itertools
import time
from numpy.random import randint


test_servo = False
test_stepper = True

servo = Servo(14)

stepper_pins = [17, 27, 22, 10] # Set the gpios being used here, in order
move = stepMotors(stepper_pins)

while True:
    print("Moving to {} deg".format(0))
    move.to_angle(0)
    servo.min()
    time.sleep(10)

    print("Moving to {} deg".format(90))
    move.to_angle(90)
    servo.max()
    time.sleep(10)


