import os
import sys
import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250
from imusensor.filters import complimentary

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

        self.imu = self._give_set_up_imu()
        # self.calibrate_sensor()
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

        self.sensorfusion.updateRollPitchYaw(
            self.imu.AccelVals[0], self.imu.AccelVals[1],
            self.imu.AccelVals[2], self.imu.GyroVals[0],
            self.imu.GyroVals[1], self.imu.GyroVals[2],
            self.imu.MagVals[0], self.imu.MagVals[1],
            self.imu.MagVals[2], dt
        )

        return [self.sensorfusion.roll, self.sensorfusion.pitch, self.sensorfusion.yaw]

    def send_outputs(self, outputs):
        for pwm_pin, output in zip(self.pwm_pins, outputs):
            pwm_pin.ChangeDutyCycle(self.base_duty + ((self.max_duty - self.base_duty)  / (conf.max_output * 2) * output))

    def reset(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.stop()
        gpio.cleanup()
