import board
import adafruit_bno055

import config as conf


class BNO055_Interface():
    def __init__(self):
        i2c = board.I2C()
        self.bno055 = adafruit_bno055.BNO055_I2C(i2c)
        self.euler = [0, 0, 0]
        self.yaw = self.correct_yaw(self.euler[0])
        self.staying_error_vertical_acc = 0
        self.faktor_adding_to_error = 0.0001

    def _give_euler(self):
        euler = self.bno055.euler
        if None in euler:
            print('None in euler')
            return self.euler
        return euler

    def give_rotor_angles(self):
        euler = self._give_euler()
        if self.is_differece_to_big(list(euler)[1:], self.euler[1:], 10):
            print('give_rotor_angles')
        else:
            self.euler = euler
            # self.euler = [euler[0] - self.base_euler[0], euler[1] - self.base_euler[1], euler[2] - self.base_euler[2]]
        return [-self.euler[1], self.euler[2], self.euler[1], -self.euler[2]]

    def give_yaw(self):
        euler = self._give_euler()
        yaw = self.correct_yaw(euler[0])
        changed_negativ_positiv = (yaw > 170 and self.yaw < -170) \
            or (yaw < -170 and self.yaw > 170)
        if changed_negativ_positiv:
            self.yaw = yaw
        elif self.is_differece_to_big([self.yaw], [yaw], 10):
            print(f'give_yaw {changed_negativ_positiv}, {yaw}, {self.yaw}')
        else:
            self.yaw = yaw
        return self.yaw

    def correct_yaw(self, yaw):
        return -360 + yaw if yaw > 180 else yaw

    def is_differece_to_big(self, new_vector, old_vector, cut_of):
        count = 0
        for new_val, val in zip(new_vector, old_vector):
            count += 1
            if abs(new_val - val) > cut_of:
                print(f'unlogical value in measurement at index {count} in ', end='')
                return True
        return False

    def give_altitude(self, previous_altitude, vertical_vel):
        linear_vertical_acceleration = self._give_linear_vertical_acceleration()
        if linear_vertical_acceleration is None:
            return previous_altitude + vertical_vel / conf.frequency
        altitude = previous_altitude + vertical_vel / conf.frequency \
            + linear_vertical_acceleration * (1/conf.frequency) ** 2 / 2
        return altitude

    def give_vertical_vel(self, previous_vertical_vel):
        linear_vertical_acceleration = self._give_linear_vertical_acceleration()
        if linear_vertical_acceleration is None:
            return previous_vertical_vel
        vertical_vel = previous_vertical_vel + linear_vertical_acceleration / conf.frequency
        return vertical_vel

    def _give_linear_vertical_acceleration(self):
        linear_acceleration = self.bno055.linear_acceleration
        gravity = self.bno055.gravity
        if None in gravity or None in linear_acceleration:
            return None
        if abs(sum(gravity) * sum(linear_acceleration)) < 0.001:
            return None
        absolut_linear_vertical_acceleration = gravity[2] / sum(gravity) * sum(linear_acceleration)
        if self.is_differece_to_big([absolut_linear_vertical_acceleration], [0], 30):
            print('_get_linear_vertical_acceleration')
            return None
        corrected_absolut_linear_vertical_acceleration  = absolut_linear_vertical_acceleration - self.staying_error_vertical_acc
        self.staying_error_vertical_acc += corrected_absolut_linear_vertical_acceleration * self.faktor_adding_to_error
        return corrected_absolut_linear_vertical_acceleration
