import time
import sys
import threading
from gpiozero import OutputDevice
from pprint import pprint


class stepMotors:
    def __init__(self, pins=[6,13,19,26], sequence=None, frequency=1000, steps_per_revolution=4096):
        '''
        Inputs:
        -----
          - pins, list[int]
            - List of pins the coils are attached to.
          - sequence, list[bool]
            - The coil sequence order. Get this from the motor datasheet!
          - frequency, float
            - How fast the motor can be driven, steps/second

        Useage:
        ... step = stepMotors(pins, seq, freq)
        ... print(step.angle)
        >>> 0.0
        ... step.angle = 180
        ... print(step.angle)
        >>> 180.0
        ... step.forward()
        >>> Motor begins spinning
        ... step.pause()
        >>> Motor stops but stays torqued
        ... step.stop()
        >>> Motor stops and torque is released
        ... step.step(1)
        >>> Motor moves one step clockwise
        ... step.cleanup()
        >>> Motor is shutdown gracefully.

        '''
        self.motorBase = []
        self.pins = pins
        for pin in self.pins:
            self.motorBase.append(OutputDevice(pin))

        # The coils need to be toggled in this order to move clockwise 1 step
        if sequence is None:
            self.seq = [
                [0,1,1,0],
                [1,1,1,0],
                [1,1,0,0],
                [1,1,0,1],
                [1,0,0,1],
                [1,0,1,1],
                [0,0,1,1],
                [0,1,1,1],
            ]
        # This counter tracks where we are in the above sequence
        self.stepCounter = 0

        # True when the motor is running
        self.state = False


        self.WAIT_TIME = 1.0/float(frequency)
        self.STEPS_PER_REV = steps_per_revolution
        self.location = 0.0

        # How close can a step get. Add 20% for numerical ease
        self.TOL = 1.2 * 360./self.STEPS_PER_REV

    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, loc):
        self._location = loc % self.STEPS_PER_REV

    @property
    def angle(self):
        a = self.location * (360./self.STEPS_PER_REV)
        return a
    @angle.setter
    def angle(self, angle):
        self.to_angle(angle)

    def cleanup(self):
        '''Grafefully shut down the motor, releasing the pins'''
        if self.thread.is_alive():
            self.state = False
            self.thread.join()

        for GpioOutputDevice in self.motorBase:
            GpioOutputDevice.off()

        return True

    def stop(self):
        '''Kill all the coils, i.e. no electrically supplied torque (gearbox will still resist)'''
        self.cleanup()

    def pause(self):
        '''Don't move the axel, but keep it torqued'''
        if self.thread.is_alive():
            self.state = False
            self.thread.join()
        return True

    def forward(self):
        '''Move forwards continuously. Non-blocking'''
        if self.state:
            self.cleanup()

        self.direction = 1

        self.state = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def backward(self):
        '''Move backwards continuously. Non-blocking'''
        if self.state:
            self.cleanup()

        self.direction = -1
        self.state = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def to_angle(self, desired_angle, direction=None, block=False):
        '''
        Inputs:
        -----
          - desired_angle, float
            - Angle is in degrees
          - direction, bool
            - +1 clockwise, -1 counterclockwise
          - block, bool
            - If True, stop the script from proceeding until the motor reaches its target

        Moves in the shortest distance, but blocked from
        crossing 359 -> 0 to prevent wires wrapping'''
        desired_angle = desired_angle % 360

        if direction is None:
            direction = -1 if self.angle > desired_angle else +1

        if block:
            self._move_to(desired_angle, direction)
        else:
            self.thread = threading.Thread(
                target=self._move_to,
                args=(desired_angle, direction)
            )
            self.thread.daemon = True
            self.thread.start()

    def _move_to(self, desired_angle, direction):
        stepCount = len(self.seq)

        dist = abs(self.angle - desired_angle)
        self.state = True
        while self.state and dist > self.TOL:
            self.step(direction)
            dist = abs(self.angle - desired_angle)
            print(dist)

    def home(self, switch):
        '''Homes the motor. Rotates until limit switch is hit by
        e.g., a cam on the shaft. Then reverses 5 degrees and slowly approaches it again.'''
        wait = self.WAIT_TIME

        while not switch.is_pressed:
            self.step(1)
        print("Hit the switch! Backing off 45 degrees...")
        # The switch is now pushed. Back off a few degrees
        for _ in range(5 * int(self.STEPS_PER_REV/360.)):
            self.step(-1)

        print("Approaching switch at 1/2 the speed...")
        # Slowly approach the limit
        while not switch.is_pressed:
            self.step(1)
            time.sleep(self.WAIT_TIME*2)
        self.location = 0
        print("Hit the switch! Location is now {}".format(self.location))

    def step(self, direction):
        '''Direction: +1 for clockwise, -1 counter clockwise'''
        stepCount=len(self.seq)
        for pin in range(0,4):
            xPin=self.motorBase[pin]

            if self.seq[self.stepCounter][pin]!=0:
                xPin.on()
            else:
                xPin.off()

        # Wait for the shaft to physically move
        time.sleep(self.WAIT_TIME)

        self.stepCounter += direction
        self.location += direction

        self.stepCounter = self.stepCounter % stepCount

    def run(self):
        while self.state:
            self.step(self.direction)
