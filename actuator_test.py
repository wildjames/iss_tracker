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
        time.sleep(5)

        move.backward()
        time.sleep(5)

        move.forward()
        time.sleep(1)

        move.backward()
        time.sleep(1)

        move.stop()


