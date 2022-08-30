import os
import sys
import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

import RPi.GPIO as gpio # this just works on a raspberry pi

from interface_control import InterfaceControl

# import config as conf     not for testing
from interface_control import InterfaceControl


class HardwareInterface(InterfaceControl):
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.frequency_I2C = 50
        self.base_duty = 8
        
        self.pwm_pins = [self._give_setup_pin(6), self._give_setup_pin(13), self._give_setup_pin(19), self._give_setup_pin(26)]
        self._set_up_output()

        self.imu = self._give_set_up_imu()
        self.calibrate_sensor()

        self.sensorfusion = kalman.Kalman()

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
        self.imu.loadCalibDataFromFile("/home/dronepi/calib_real_bolder.json")

    def calibrate_sensor(self):
        self.imu.caliberateAccelerometer()
        print ("Acceleration calib successful")

        #self.imu.caliberateMagPrecise()
        #print ("Mag calib successful")

        # TODO: write the calibration

    def _set_up_output(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.start(self.base_duty)

        time.sleep(5)

    def _give_setup_pin(self, pin_number):
        gpio.setup(pin_number, gpio.OUT)
        pwm = gpio.PWM(pin_number, self.frequency_I2C)
        return pwm

    def give_measurements(self):
        self.imu.readSensor()
        self.imu.computeOrientation()

        newTime = time.time()
        dt = newTime - self.current_time
        self.current_time = newTime

        self.sensorfusion.computeAndUpdateRollPitchYaw(
            self.imu.AccelVals[0], self.imu.AccelVals[1],
            self.imu.AccelVals[2], self.imu.GyroVals[0],
            self.imu.GyroVals[1], self.imu.GyroVals[2],
            self.imu.MagVals[0], self.imu.MagVals[1],
            self.imu.MagVals[2], dt
        )

        return [self.sensorfusion.roll, self.sensorfusion.pitch, self.sensorfusion.yaw]

    def send_outputs(self, outputs):
        # TODO: this has to be redone
        for pwm_pin, output in zip(self.pwm_pins, outputs):
            # output += conf.max_ouptput / 2    not for testing
            print(round(self.base_duty + output / 1000, 3))
            pwm_pin.ChangeDutyCycle(self.base_duty + output / 1000)

    def reset(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.stop()
        gpio.cleanup()
