from gpiozero import Servo, OutputDevice
from time import sleep
from stepper import stepMotors
import pigpio
import itertools
import time
from numpy.random import randint


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
        # move.forward()
        # stop = time.perf_counter() + 5
        # while time.perf_counter() < stop:
        #     print("Stepper location: {: <6d}".format(move.location), end='\r')

        # move.backward()
        # stop = time.perf_counter() + 5
        # while time.perf_counter() < stop:
        #     print("Stepper location: {: <6d}".format(move.location), end='\r')

        # move.forward()
        # stop = time.perf_counter() + 1
        # while time.perf_counter() < stop:
        #     print("Stepper location: {: <6d}".format(move.location), end='\r')

        # move.backward()
        # stop = time.perf_counter() + 1
        # while time.perf_counter() < stop:
        #     print("Stepper location: {: <6d}".format(move.location), end='\r')

        # move.pause()
        # time.sleep(2)

        print("\nMoving to {} deg".format(0))
        move.to_angle(0)
        time.sleep(10)
        # stop = time.perf_counter() + 10
        # while time.perf_counter() < stop:
        #     print("Stepper location: {: <8.3f}".format(move.angle), end='\r')

        print("\nMoving to {} deg".format(5))
        move.to_angle(5)
        time.sleep(10)
        # stop = time.perf_counter() + 10
        # while time.perf_counter() < stop:
        #     print("Stepper location: {: <8.3f}".format(move.angle), end='\r')

        # randloc = randint(360)
        # print("\nMoving to {} deg".format(randloc))
        # move.to_angle(randloc)
        # stop = time.perf_counter() + 10
        # while time.perf_counter() < stop:
        #     print("Stepper location: {: <8.3f}".format(move.angle), end='\r')


