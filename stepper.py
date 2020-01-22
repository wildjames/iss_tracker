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

        # The coils need to be toggled in this order
        self.seq = [
            [1,0,1,0],
            [1,0,0,1],
            [0,1,0,1],
            [0,1,1,0]
        ]

        self.state = False

    def cleanup(self):
        if self.thread.is_alive():
            self.state = False
            self.thread.join()

        for GpioOutputDevice in self.motorBase:
            GpioOutputDevice.off()

        return True

    def stop(self):
        if self.state:
            self.cleanup()

    def forward(self):
        if self.state:
            self.cleanup()

        self.direction = 1
        self.stepCounter = 0

        self.state = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def backward(self):
        if self.state:
            self.cleanup()

        self.direction = -1
        self.stepCounter = 0
        self.state = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        waitTime = 0.001
        stepCount=len(self.seq)

        while self.state:
            for pin in range(0,4):
                xPin=self.motorBase[pin]

                if self.seq[self.stepCounter][pin]!=0:
                    xPin.on()
                else:
                    xPin.off()

            time.sleep(waitTime)

            self.stepCounter += self.direction

            if self.stepCounter >= stepCount:
                self.stepCounter = 0

            if self.stepCounter < 0:
                self.stepCounter = stepCount+self.direction
