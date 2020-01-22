from gpiozero import Servo, OutputDevice
from time import sleep
from stepper import stepper
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
    # The stepper should move clockwise then
    # anti-clockwise for DELAY seconds.

    DELAY = 3

    gpios = [17, 27, 22, 10] # Set the gpios being used here.

    pi=pigpio.pi()

    if not pi.connected:
        exit(0)

    try:
        s = stepper(pi, *gpios)

        stop = time.time() + DELAY
        while time.time() < stop:
            s.forward()
            time.sleep(0.0001)

        stop = time.time() + DELAY
        while time.time() < stop:
            s.backward()
            time.sleep(0.0001)

    except KeyboardInterrupt:
        pass

    s.stop()

    pi.stop()

