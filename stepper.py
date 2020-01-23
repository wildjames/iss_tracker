import time
import sys
import threading
from gpiozero import OutputDevice
from pprint import pprint


class stepMotors:
    def __init__(self, pins=[6,13,19,26]):
        self.motorBase = []
        self.pins = pins
        for pin in self.pins:
            self.motorBase.append(OutputDevice(pin))

        # The coils need to be toggled in this order to move clockwise 1 step
        self.seq = [
            [0,1,1,1],
            [0,0,1,1],
            [1,0,1,1],
            [1,0,0,1],
            [1,1,0,1],
            [1,1,0,0],
            [1,1,1,0],
            [0,1,1,0],
        ]
        self.stepCounter = 0

        self.state = False

        self.WAIT_TIME = 1/1000.
        self.STEPS_PER_REV = 4096.
        self.location = 0.0

        # How close can a step get. Add 50% for numerical ease
        self.TOL = 1.5 * 360./self.STEPS_PER_REV

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

    def cleanup(self):
        if self.thread.is_alive():
            self.state = False
            self.thread.join()

        for GpioOutputDevice in self.motorBase:
            GpioOutputDevice.off()

        return True

    def stop(self):
        '''Kill all the coils, i.e. no electrically supplied torque (gearbox will still resist)'''
        if self.state:
            self.cleanup()

    def pause(self):
        '''Don't move the axel, but keep it torqued'''
        if self.thread.is_alive():
            self.state = False
            self.thread.join()
        return True

    def forward(self):
        if self.state:
            self.cleanup()

        self.direction = 1

        self.state = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def backward(self):
        if self.state:
            self.cleanup()

        self.direction = -1
        self.state = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def to_angle(self, desired_angle, direction=None, block=False):
        '''Desired angle is in degrees'''
        desired_angle = desired_angle % 360

        if direction is None:
            self.direction = +1 if self.angle > desired_angle else -1

        self._desired_angle = desired_angle

        self.state = True
        if block:
            self._move_to()
        else:
            self.thread = threading.Thread(target=self._move_to, args=())
            self.thread.daemon = True
            self.thread.start()

    def _move_to(self):
        stepCount = len(self.seq)

        dist = abs(self.angle - self._desired_angle)
        while self.state and dist > self.TOL:
            for pin in range(0,4):
                xPin=self.motorBase[pin]

                if self.seq[self.stepCounter][pin]!=0:
                    xPin.on()
                else:
                    xPin.off()

            time.sleep(self.WAIT_TIME)

            self.stepCounter += self.direction
            self.location += self.direction

            self.stepCounter = self.stepCounter % stepCount

            dist = abs(self.angle - self._desired_angle)
            print(dist)

    def run(self):
        stepCount=len(self.seq)

        while self.state:
            for pin in range(0,4):
                xPin=self.motorBase[pin]

                if self.seq[self.stepCounter][pin]!=0:
                    xPin.on()
                else:
                    xPin.off()

            time.sleep(self.WAIT_TIME)

            self.stepCounter += self.direction
            self.location += self.direction

            if self.stepCounter >= stepCount:
                self.stepCounter = 0

            if self.stepCounter < 0:
                self.stepCounter = stepCount+self.direction
