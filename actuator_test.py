from gpiozero import Servo, OutputDevice
from time import sleep
from stepper import stepMotors
import pigpio
import itertools
import time


test_servo = False
test_stepper = True

if test_servo:
    servo = Servo(14)

    while True:
        servo.min()
        sleep(1)
        servo.mid()
        sleep(1)
        servo.max()
        sleep(1)


if test_stepper:
    gpios = [17, 27, 22, 10] # Set the gpios being used here, in order

    move = stepMotors(gpios)
    while True:
        move.forward()
        stop = time.clock() + 5
        while time.clock() < stop:
            print("Stepper location: {: <6d}".format(move.location), end='\r')

        move.backward()
        stop = time.clock() + 5
        while time.clock() < stop:
            print("Stepper location: {: <6d}".format(move.location), end='\r')

        move.forward()
        stop = time.clock() + 1
        while time.clock() < stop:
            print("Stepper location: {: <6d}".format(move.location), end='\r')

        move.backward()
        stop = time.clock() + 1
        while time.clock() < stop:
            print("Stepper location: {: <6d}".format(move.location), end='\r')

        move.stop()


