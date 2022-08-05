import Rpi.GPIO as gpio # this just works on a raspberry pi
from time import sleep

from interface_control import InterfaceControl



class InterfaceHardware(InterfaceControl):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.frequency_I2C = 50
        self.base_duty = 5000

        self.pwm_pins = [_give_setup_pin(22), _give_setup_pin(23), _give_setup_pin(26), _give_setup_pin(20)]


    def _set_up_output(self):
        for pwm_pin in pwm_pins:
            pwm_pin.start(self.base_duty)

        time.sleep(5)

    def _give_setup_pin(pin_number):
        GPIO.setup(pin_number, GPIO.OUT)
        pwm = GPIO.PWM(pin_number, self.frequency_I2C)
        return pwm

    def give_measurements(self):
        pass

    def send_outputs(self, outputs):
        for pin_rotor, output in zip(self.pwm_pins, outputs):
            self.pin_rotor.duty_u16(base_duty + output)
