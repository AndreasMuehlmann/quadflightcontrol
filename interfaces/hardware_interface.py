import sys

from bno055_interface import BNO055_Interface
from pwm_interface import PWM_Interface
from bmp280_interface import BMP280_Interface
from complimentary_filter import ComplimentaryFilter


class HardwareInterface():
    def __init__(self):
        try:
            self.imu_interface = BNO055_Interface()
            self.baro_interface = BMP280_Interface()
            self.output_interface = PWM_Interface()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        self.previous_height_vel = 0
        self.complimentary_filter = ComplimentaryFilter(0.8)

    def give_rotor_angles(self):
        try:
            return self.imu_interface.give_rotor_angles()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting rotor angles:')
            print(e)

    def give_rotation(self):
        try:
            return self.imu_interface.give_rotation()

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting yaw:')
            print(e)

    def give_height_vel(self):
        try:
            baro_height_vel = self.bmp280_interface.give_height_vel()
            accelerometer_height_vel = self.bno055_interface.give_height_vel(self.previous_height_vel)

        except KeyboardInterrupt:
            self.reset()
            sys.exit()

        except Exception as e:
            print('in getting height_vel:')
            print(e)

        height_vel = self.complimentary_filter.fuse(accelerometer_height_vel, baro_height_vel)
        self.previous_height_vel = height_vel
        return height_vel

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
