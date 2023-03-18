import sys
import time
from copy import deepcopy
import smbus
import numpy as np

import busio
import board
import adafruit_pca9685

import config as conf
from bno055_interface import BNO055_Interface
from pwm_interface import PWM_Interface


class HardwareInterface():
    def __init__(self):
        try:
            self.measurement_interface = BNO055_Interface()
            self.output_interface = PWM_Interface()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

    def give_rotor_angles(self):
        try:
            return self.measurement_interface.give_rotor_angles()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting rotor angles:')
            print(e)

    def give_rotation(self):
        try:
            return self.measurement_interface.give_rotation()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting yaw:')
            print(e)

    def send_outputs(self, outputs):
        try: 
            self.output_interface.send_outputs(outputs) 

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('In changing duty cycle:')
            print(e)

    def reset(self):
        self.output_interface.reset()
