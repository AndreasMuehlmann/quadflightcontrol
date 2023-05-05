import sys
import time
import traceback

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

        self.altitude_complimentary_filter = ComplimentaryFilter(0.7)
        self.altitude = self.baro_interface.give_altitude()
        self.vertical_vel = 0
        self.previous_vertical_vel = 0
        self.vertical_vel_complimentary_filter = ComplimentaryFilter(0.7)

    def give_rotor_angles(self):
        try:
            return self.imu_interface.give_rotor_angles()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print(traceback.format_exc())

    def give_yaw(self):
        try:
            return self.imu_interface.give_yaw()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print(traceback.format_exc())

    def give_altitude(self):
        try:
            accelerometer_altitude = self.imu_interface.give_altitude(self.altitude, self.give_vertical_vel())
            baro_altitude = self.baro_interface.give_altitude()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print(traceback.format_exc())

        self.altitude = self.altitude_complimentary_filter.fuse(accelerometer_altitude, baro_altitude)
        return self.altitude

    def give_vertical_vel(self):
        try:
            accelerometer_vertical_vel = self.imu_interface.give_vertical_vel(self.previous_vertical_vel)
            baro_vertical_vel = self.baro_interface.give_vertical_vel()
        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print(traceback.format_exc())

        vertical_vel = self.vertical_vel_complimentary_filter.fuse(accelerometer_vertical_vel, baro_vertical_vel)
        self.previous_vertical_vel = vertical_vel
        return vertical_vel


    def send_outputs(self, outputs):
        try:
            self.output_interface.send_outputs(outputs)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print(traceback.format_exc())

    def reset(self):
        self.output_interface.reset()
