import sys
import time

import busio
import board
import adafruit_pca9685

import config as conf


class PWM_Interface():
    def __init__(self):
        self.pwm_range = 0xffff
        self.prozent_to_duty_cycle = self.pwm_range / 100
        self.base_duty = 40 * self.prozent_to_duty_cycle
        self.max_duty = 80 * self.prozent_to_duty_cycle

        i2c = busio.I2C(board.SCL, board.SDA)
        pwm_generator = adafruit_pca9685.PCA9685(i2c)
        pwm_generator.frequency = 400
        self.pwm_pins = [pwm_generator.channels[i] for i in range(4)]

        # self._calibrate_motor_controllers()
        self._boot_motor_controller()

    def _boot_motor_controller(self):
        try:
            for pwm_pin in self.pwm_pins:
                pwm_pin.duty_cycle = int(self.base_duty)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        time.sleep(1)

    def _calibrate_motor_controllers(self):
        input("CALIBRATION")
        try:
            for pwm_pin in self.pwm_pins:
                pwm_pin.duty_cycle = int(self.max_duty)
            time.sleep(5)

            input("wait until beeping ends")

            for pwm_pin in self.pwm_pins:
                pwm_pin.duty_cycle = int(self.base_duty)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        time.sleep(5)

        input("wait until beeping ends")

        print("motor controllers are calibrated")

    def send_outputs(self, outputs):
        for pwm_pin, output in zip(self.pwm_pins, outputs):
            duty_cycle = self.base_duty + ((self.max_duty - self.base_duty)  / (conf.max_output) * output)
            pwm_pin.duty_cycle = round(duty_cycle)

    def reset(self, counter=0):
        try:
            for pwm_pin in self.pwm_pins:
                pwm_pin.duty_cycle = 0

        except Exception as e:
            print('In resetting:')
            print(e)

            time.sleep(0.1)
            if counter < 5:
                self.reset(counter + 1)
