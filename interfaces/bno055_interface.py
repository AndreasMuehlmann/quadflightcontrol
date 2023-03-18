import time

import board
import adafruit_bno055


class BNO055_Interface():
    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        time.sleep(2)
        self.base_euler = self.sensor.euler

        self.euler = [0, 0, 0]

        self.rotation = self.calc_rotation(self.base_euler)

    def give_rotor_angles(self):
        new_euler = self.sensor.euler
        if None in new_euler or self.is_differece_to_big(list(new_euler)[1:], self.euler[1:], 30):
            print('None in euler')
        else:
            self.euler = [new_euler[0] - self.base_euler[0], new_euler[1] - self.base_euler[1], new_euler[2] - self.base_euler[2]]

        return [-self.euler[1], self.euler[2], self.euler[1], -self.euler[2]]


    def give_rotation(self):
        new_euler = self.sensor.euler
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
