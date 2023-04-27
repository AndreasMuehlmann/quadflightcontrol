import time

import board
import adafruit_bno055

import config as conf


class BNO055_Interface():
    def __init__(self):
        i2c = board.I2C()
        self.bno055 = adafruit_bno055.BNO055_I2C(i2c)
        time.sleep(2)
        self.base_euler = self.bno055.euler

        self.euler = [0, 0, 0]

        self.yaw = self.correct_yaw(self.base_euler[0])

    def give_rotor_angles(self):
        new_euler = self.bno055.euler
        if None in new_euler:
            print('None in euler')
        elif self.is_differece_to_big(list(new_euler)[1:], self.euler[1:], 30):
            print('give_rotor_angles')
        else:
            self.euler = [new_euler[0] - self.base_euler[0], new_euler[1] - self.base_euler[1], new_euler[2] - self.base_euler[2]]

        return [-self.euler[1], self.euler[2], self.euler[1], -self.euler[2]]

    def give_yaw(self):
        new_euler = self.bno055.euler
        if None in new_euler:
            print('None in euler')
            return self.yaw
        new_yaw = self.correct_yaw(new_euler[0])
        if self.is_differece_to_big([self.yaw], [new_yaw], 10):
            print('give_rotation')
            return self.yaw
        self.yaw = new_yaw
        return self.yaw

    def correct_yaw(self, yaw):
        new_yaw = yaw - self.base_euler[0]
        new_yaw = -360 + new_yaw if new_yaw > 180 else new_yaw
        return new_yaw

    def is_differece_to_big(self, new_vector, old_vector, cut_of):
        count = 0
        for new_val, val in zip(new_vector, old_vector):
            count += 1
            if abs(new_val - val) > cut_of:
                print(f'unlogical value in measurement at index {count} in ', end='')
                return True
        return False

    def give_altitude(self, previous_altitude, altitude_vel):
        #print(f'{time.time()},{self.bno055.linear_acceleration[0]},{self.bno055.linear_acceleration[1]},{self.bno055.linear_acceleration[2]}')
        linear_acceleration = self.bno055.linear_acceleration
        gravity = self.bno055.gravity
        if None in gravity or None in linear_acceleration:
            print('None in gravity or linear_acceleration')
            return self.altitude + self.altitude_vel * 1 / conf.frequency
        absolut_linear_height_acceleration = gravity[2] / sum(gravity) * sum(linear_acceleration)
        if self.is_differece_to_big([absolut_linear_height_acceleration], [0], 30):
            print('give_altitude')
            return self.altitude + self.altitude_vel * 1 / conf.frequency
        altitude = altitude_vel * conf.frequency + absolut_linear_height_acceleration *  conf.frequency**2 / 2
        # print(f'{[round(ala, 2) for ala in absolut_linear_height_acceleration] }')
        return altitude
