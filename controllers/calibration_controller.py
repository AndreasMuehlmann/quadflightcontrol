import time

import config as conf


class CalibrationController:
    def __init__(self):
        self.time_between_motor_calibrations = 10
        self.calibrated_motor = 0
        self.output = 400
        self.end_output = 700
        self.output_increase_per_second = 10
        self.angle_when_lifted = 5
        self.sleep_start_time = 0
        self.sleep_time = 10

        self.rotor_outputs_angle_controllers = [0, 0, 0, 0]
        self.yaw_controller_output = 0
        self.altitude_controller_output = 0

    def give_outputs(self, inputs, rotor_angles, yaw, altitude):
        outputs = [0, 0, 0, 0]
        if self.sleep_time > time.time() - self.sleep_start_time:
            return outputs
        if self.is_lifted(rotor_angles):
            print(f'rotor {self.calibrated_motor} lift output: {self.output}')
            self.sleep_start_time = time.time()
            return outputs
        self.output += self.output_increase_per_second / conf.frequency
        outputs[self.calibrated_motor] = self.output
        return outputs

    def is_lifted(self, rotor_angles):
        return max(rotor_angles) > self.angle_when_lifted
