import RPi.GPIO as gpio # this just works on a raspberry pi
from time import sleep

from interface_control import InterfaceControl
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250


class HardwareInterface(InterfaceControl):
    def __init__(self):
        gpio.setmode(gpio.BOARD)
        self.frequency_I2C = 50
        self.base_duty = 5000

        self.pwm_pins = [_give_setup_pin(22), _give_setup_pin(23), _give_setup_pin(26), _give_setup_pin(20)]

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
        for pwm_pin in pwm_pins:
            pwm_pin.start(self.base_duty)

        time.sleep(5)

    def _give_setup_pin(pin_number):
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
        for pin_rotor, output in zip(self.pwm_pins, outputs):
            self.pin_rotor.duty_u16(base_duty + output)
