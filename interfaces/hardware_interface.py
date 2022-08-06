from time import sleep

import RPi.GPIO as gpio # this just works on a raspberry pi
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

# import config as conf     not for testing
from interface_control import InterfaceControl


class HardwareInterface(InterfaceControl):
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.frequency_I2C = 50
        self.base_duty = 7
        
        self.pwm_pins = [self._give_setup_pin(6), self._give_setup_pin(13), self._give_setup_pin(19), self._give_setup_pin(26)]
        self._set_up_output()

        self.mpu = self._give_set_up_mpu_sensor()

    def _give_set_up_mpu_sensor(self):
        mpu = MPU9250(
            address_ak=AK8963_ADDRESS,
            address_mpu_master=MPU9050_ADDRESS_68,
            address_mpu_slave=None,
            bus=1,
            gfs=GFS_1000,
            afs=AFS_8G,
            mfs=AK8963_BIT_16,
            mode=AK8963_MODE_C100HZ)

        mpu.configure()
        return mpu

    def _set_up_output(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.start(self.base_duty)

        sleep(5)

    def _give_setup_pin(self, pin_number):
        gpio.setup(pin_number, gpio.OUT)
        pwm = gpio.PWM(pin_number, self.frequency_I2C)
        return pwm

    def give_measurements(self):
        print("Accelerometer", mpu.readAccelerometerMaster())
        print("Gyroscope", mpu.readGyroscopeMaster())
        print("Magnetometer", mpu.readMagnetometerMaster())
        print("Temperature", mpu.readTemperatureMaster())
        print("\n")

    def send_outputs(self, outputs):
        for pwm_pin, output in zip(self.pwm_pins, outputs):
            # output += conf.max_ouptput / 2    not for testing
            print(round(self.base_duty + output / 1000, 3))
            pwm_pin.ChangeDutyCycle(self.base_duty + output / 1000)

    def reset(self):
        for pwm_pin in self.pwm_pins:
            pwm_pin.stop()
        gpio.cleanup()
