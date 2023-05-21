import board
import adafruit_bno055

import config as conf

from measurement_validator import Measurement_Validator


class BNO055_Interface():
    def __init__(self):
        i2c = board.I2C()
        self.bno055 = adafruit_bno055.BNO055_I2C(i2c)
        self.euler = [0, 0, 0]
        self.yaw = self.correct_yaw(self.euler[0])
        self.correction_roll = 0
        self.correction_pitch = 0
        self.staying_error_vertical_acc = -0.25
        self.faktor_adding_to_error = 0.001
        self.measurement_validator_yaw = Measurement_Validator(2, 15)
        self.measurement_validator_roll = Measurement_Validator(2, 15)
        self.measurement_validator_pitch = Measurement_Validator(2, 15)
        self.measurement_validator_absolut_linear_vertical_acceleration = Measurement_Validator(30, 60)

    def _give_euler(self):
        euler = self.bno055.euler
        if None in euler:
            print('None in euler')
            return self.euler
        return [euler[0], euler[1] - self.correction_roll, euler[2] - self.correction_pitch]

    def give_rotor_angles(self):
        euler = self._give_euler()
        roll = self.measurement_validator_roll.give_validatet_measurement(euler[1])
        pitch = self.measurement_validator_pitch.give_validatet_measurement(euler[2])
        return [-roll, pitch]

    def give_yaw(self):
        euler = self._give_euler()
        yaw = self.correct_yaw(euler[0])
        if abs(yaw) > 180:
            return self.yaw
        changed_negativ_positiv = (yaw > 170 and self.yaw < -170) \
            or (yaw < -170 and self.yaw > 170)
        if changed_negativ_positiv:
            self.measurement_validator_yaw.measurement = yaw
        else:
            yaw = self.measurement_validator_yaw.give_validatet_measurement(yaw)
        self.yaw = yaw
        return self.yaw

    def correct_yaw(self, yaw):
        return -360 + yaw if yaw > 180 else yaw

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
        self.measurement_validator_absolut_linear_vertical_acceleration.give_validatet_measurement(absolut_linear_vertical_acceleration)
        corrected_absolut_linear_vertical_acceleration  = absolut_linear_vertical_acceleration - self.staying_error_vertical_acc
        self.staying_error_vertical_acc += corrected_absolut_linear_vertical_acceleration * self.faktor_adding_to_error
        return corrected_absolut_linear_vertical_acceleration
