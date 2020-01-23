'''The gpiozero servo implimentation is shite'''

class Servo():
    def __init__(self, pin, initial_value=0, min_pulse=1e-6, max_pulse=2e-6, frame_width=20e-6):
        '''
        Inputs:
        -----
          - pin, int
            - The pin connected to the data of the servo
          - initial_value, float
            - Initial location for the servo. Safe range 0:+1
          - min_pulse, float
            - Minimum pulse width registered by the servo, in microseconds
          - max_pulse, float
            - as above
          - frame_width, float
            - Width of a frame. 1/fequency, in microseconds
            '''
        self._pi = pigpio.pi()

        self.pin = pin
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.frame_width = frame_width

        self.value = initial_value


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

        val = 500. + (value*2000.)
        self._pi.set_servo_pulsewidth(self.pin, val)