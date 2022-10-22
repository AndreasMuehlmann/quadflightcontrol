import sys
import time
from copy import deepcopy
import smbus
import numpy as np

import board
import busio
import adafruit_bno055
import adafruit_pca9685

import config as conf


class HardwareInterface():
    def __init__(self):
        self.pwm_range = 0xffff
        self.prozent_to_duty_cycle = self.pwm_range / 100
        self.base_duty = 40 * self.prozent_to_duty_cycle
        self.max_duty = 80 * self.prozent_to_duty_cycle

        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            pwm_generator = adafruit_pca9685.PCA9685(i2c)
            pwm_generator.frequency = 400
            self.pwm_pins = [pwm_generator.channels[i] for i in range(4)]

            # self._calibrate_motor_controllers()
            self._boot_motor_controller()

            i2c = board.I2C()
            self.sensor = adafruit_bno055.BNO055_I2C(i2c)
            time.sleep(2)
            self.base_euler = self.sensor.euler

            self.euler = [0, 0, 0]

            self.rotation = self.calc_rotation(self.base_euler)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

    def give_rotor_angles(self):
        try:
            new_euler = self.sensor.euler
            
        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting rotor angles:')
            print(e)

        if None in new_euler or self.is_differece_to_big(list(new_euler)[1:], self.euler[1:], 30):
            print('None in euler')
        else:
            self.euler = [new_euler[0] - self.base_euler[0], new_euler[1] - self.base_euler[1], new_euler[2] - self.base_euler[2]]

        return [-self.euler[1], self.euler[2], self.euler[1], -self.euler[2]]


    def give_rotation(self):
        try:
            new_euler = self.sensor.euler
            
        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting yaw:')
            print(e)
    
        if None in new_euler:
            print('None in euler')
        elif self.is_differece_to_big([self.calc_rotation(new_euler)], [self.rotation], 30) \
                and not (self.calc_rotation(new_euler) > 100 and self.rotation < -100):
            print('wrong measurement in give_rotation')
        else:
            self.rotation = self.calc_rotation(new_euler)

        return self.rotation

    def calc_rotation(self, euler):
        yaw = euler[0] - self.base_euler[0]
        rotation = -360 + yaw if yaw > 180 else yaw
        return rotation

    def is_differece_to_big(self, new_vector, old_vector, cut_of):
        count = 0
        for new_val, val in zip(new_vector, old_vector):
            count  += 1
            if abs(new_val - val) > cut_of:
                print(f'error in euler {count}')
                return True
        return False

    def _boot_motor_controller(self):
        try:
            for pwm_pin in self.pwm_pins:
                pwm_pin.duty_cycle = int(self.base_duty)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        time.sleep(2)

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
        try: 
            for pwm_pin, output in zip(self.pwm_pins, outputs):
                duty_cycle = self.base_duty + ((self.max_duty - self.base_duty)  / (conf.max_output * 2) * output)
                pwm_pin.duty_cycle = round(duty_cycle)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('In changing duty cycle:')
            print(e)

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
