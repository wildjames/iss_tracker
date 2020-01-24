'''The gpiozero servo implimentation is shite'''
import pigpio


class Servo():
    def __init__(self, pin, initial_value=0, min_angle=0, max_angle=180, min_allowed=None, max_allowed=None):
        '''
        Inputs:
        -----
          - pin, int
            - The pin connected to the data of the servo
          - initial_value, float
            - Initial location for the servo. Safe range 0:+1
          - min_angle, float
            - Minimum angle reachable by the servo, in degrees
          - max_angle, float
            - as above
            '''
        self._pi = pigpio.pi()

        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle

        if min_allowed is None or min_allowed < min_angle:
            min_allowed = min_angle
        if max_allowed is None or max_allowed > max_angle:
            max_allowed = max_angle

        self.min_allowed = min_allowed
        self.max_allowed = max_allowed

        self.value = initial_value


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        '''0:1. Also None, to disengage the servo'''
        if value is None:
            value = 0

        self._value = value

        val = 500. + (value*2000.)
        self._pi.set_servo_pulsewidth(self.pin, val)

    @property
    def angle(self):
        angle = self.min_angle + (self._value * (self.max_angle - self.min_angle))
        return angle

    @angle.setter
    def angle(self, angle):
        '''Angle is in degrees'''
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle

        if angle < self.min_allowed:
            angle = self.min_allowed
        elif angle > self.max_allowed:
            angle = self.max_allowed

        val = (angle - self.min_angle)/(self.max_angle - self.min_angle)

        self.value = 1. - val

    def close(self):
        self._pi.set_servo_pulsewidth(self.pin, 0)
