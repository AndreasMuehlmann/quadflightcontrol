import sys
import time

import config as conf
from bno055_interface import BNO055_Interface
from pwm_interface import PWM_Interface
from bmp280_interface import BMP280_Interface
from complimentary_filter import ComplimentaryFilter


class HardwareInterface():
    def __init__(self):
        try:
            self.output_interface = PWM_Interface()
            self.imu_interface = BNO055_Interface()
            self.baro_interface = BMP280_Interface()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        self.complimentary_filter = ComplimentaryFilter(0.5)
        time.sleep(0.5)
        self.altitude = self.baro_interface.give_altitude()
        self.base_altitude = self.altitude
        self.altitude_vel = 0

    def give_rotor_angles(self):
        try:
            return self.imu_interface.give_rotor_angles()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting rotor angles:')
            print(e)

    def give_yaw(self):
        try:
            return self.imu_interface.give_yaw()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting yaw:')
            print(e)

    def give_height_vel(self):
        try:
            accelerometer_altitude = self.imu_interface.give_height_vel(self.altitude, self.altitude_vel)
            baro_altitude = self.baro_interface.give_altitude(self.base_altitude)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting height_vel:')
            print(e)

        altitude = self.complimentary_filter.fuse(accelerometer_altitude, baro_altitude)
        self.altitude_vel = (altitude - self.altitude) * conf.frequency
        self.altitude = altitude
        print(round(self.altitude))
        return self.altitude

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
