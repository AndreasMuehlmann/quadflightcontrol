import os
import sys
import time
from copy import deepcopy
import smbus
import numpy as np

import board
import busio
import adafruit_bno055
import adafruit_pca9685

from interface_control import InterfaceControl

import config as conf # not for testing
from interface_control import InterfaceControl


class HardwareInterface(InterfaceControl):
    def __init__(self):
        self.calibration_file_path = '/home/dronepi/programming/quadflightcontrol/interfaces/sensor_calib.json'

        self.pwm_range = 0xffff
        self.prozent_to_duty_cycle = self.pwm_range / 100
        self.base_duty = 5 * self.prozent_to_duty_cycle
        self.max_duty = 10 * self.prozent_to_duty_cycle

        i2c = busio.I2C(board.SCL, board.SDA)
        pwm_generator = adafruit_pca9685.PCA9685(i2c)
        pwm_generator.frequency = 50

        self.pwm_pins = [pwm_generator.channels[i] for i in range(4)]
        self._boot_motor_controller()

        i2c = board.I2C()
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        time.sleep(2)
        self.vector = [0, 0, 0, 0]
        self.base_euler = self.sensor.euler

    def give_measurements(self):
        euler = self.sensor.euler

        if None in euler or self.is_differece_to_big(list(euler)[1:]):
            print('\n\nError in measuring\n\n')
        else:
            self.vector = [euler[0] - self.base_euler[0], euler[1] - self.base_euler[1], euler[2] - self.base_euler[2]]

        return [-self.vector[1], self.vector[2], self.vector[1], -self.vector[2]]

    def is_differece_to_big(self, new_vector):
        count = 0
        for new_val, val in zip(new_vector, self.vector[1:]):
            count  += 1
            if abs(new_val - val) > 30:
                print(f'error in euler {count}')
                return True
        return False

    def _boot_motor_controller(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.duty_cycle = int(self.base_duty)

        time.sleep(5)

    def send_outputs(self, outputs):
        for pwm_pin, output in zip(self.pwm_pins, outputs):
            duty_cycle = self.base_duty + ((self.max_duty - self.base_duty)  / (conf.max_output * 2) * output)
            pwm_pin.duty_cycle = round(duty_cycle)

    def reset(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.duty_cycle = 0
