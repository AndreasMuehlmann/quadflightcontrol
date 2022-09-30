import os
import sys
import time
from copy import deepcopy
import smbus
import numpy as np

import adafruit_bno055
import board

'''
from imusensor.MPU9250 import MPU9250
from imusensor.filters import complimentary
'''

import RPi.GPIO as gpio # this just works on a raspberry pi

from interface_control import InterfaceControl

import config as conf # not for testing
from interface_control import InterfaceControl


class HardwareInterface(InterfaceControl):
    def __init__(self):
        self.calibration_file_path = '/home/dronepi/programming/quadflightcontrol/interfaces/sensor_calib.json'
        gpio.setmode(gpio.BCM)
        self.frequency_I2C = 50
        self.base_duty = 5
        self.max_duty = 9
        
        self.pwm_pins = [self._give_setup_pin(6), self._give_setup_pin(13), self._give_setup_pin(19), self._give_setup_pin(26)]
        self._set_up_output()

        i2c = board.I2C()
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        time.sleep(2)
        self.vector = [0, 0, 0, 0]
        self.base_euler = self.sensor.euler

        '''
        self.imu = self._give_set_up_imu()
        self.calibrate_sensor()
        self.read_calibration()


        self.sensorfusion = complimentary.Complimentary(0.3)

        self.imu.readSensor()
        self.imu.computeOrientation()
        self.sensorfusion.roll = self.imu.roll
        self.sensorfusion.pitch = self.imu.pitch
        self.sensorfusion.yaw = self.imu.yaw

        self.current_time = time.time()

    def _give_set_up_imu(self):
        address = 0x68
        bus = smbus.SMBus(1)
        imu = MPU9250.MPU9250(bus, address)
        imu.begin()
        return imu

    def read_calibration(self):
        self.imu.loadCalibDataFromFile(self.calibration_file_path)

    def calibrate_sensor(self):
        self.imu.caliberateAccelerometer()
        print ("Acceleration calib successful")

        # Magnetometer not working
        #self.imu.caliberateMagPrecise()
        #print ("Mag calib successful")

        self.imu.saveCalibDataToFile(self.calibration_file_path)

        '''
    def _set_up_output(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.start(self.base_duty)

        time.sleep(5)

    def _give_setup_pin(self, pin_number):
        gpio.setup(pin_number, gpio.OUT)
        pwm = gpio.PWM(pin_number, self.frequency_I2C)
        return pwm

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
            if abs(new_val - val) > 20:
                print(f'error in {count}')
                return True
        return False
        

    '''
    def give_measurements(self):
        self.imu.readSensor()
        self.imu.computeOrientation()

        newTime = time.time()
        dt = newTime - self.current_time
        self.current_time = newTime


        self.sensorfusion.updateRollPitchYaw(self.imu.roll, self.imu.pitch,
                                             self.imu.yaw, self.imu.GyroVals[0],
                                             self.imu.GyroVals[1], self.imu.GyroVals[2], dt)

        orientation = [self.sensorfusion.roll, self.sensorfusion.pitch, self.sensorfusion.yaw]
        roll = 180 - abs(orientation[0])
        if orientation[0] < 0:
            roll *= -1

        pitch = orientation[1]

        measurements = [pitch, roll, -pitch, -roll]

        return measurements
    '''

    def send_outputs(self, outputs):
        for pwm_pin, output in zip(self.pwm_pins, outputs):
            pwm_pin.ChangeDutyCycle(self.base_duty + ((self.max_duty - self.base_duty)  / (conf.max_output * 2) * output))

    def reset(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.stop()
        gpio.cleanup()
