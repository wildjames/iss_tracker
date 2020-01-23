'''The gpiozero servo implimentation is shite'''
import pigpio


class Servo():
    def __init__(self, pin, initial_value=0, min_angle=0, max_angle=180):
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
        val = (angle - self.min_angle)/(self.max_angle - self.min_angle)
        self.value = val

    def close(self):
        self._pi.set_servo_pulsewidth(17, 0)
        self._pi.close()