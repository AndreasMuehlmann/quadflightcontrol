import numpy as np

from controller_env import ControllerEnv


class VelEnv(ControllerEnv):
    def __init__(self):
        super(VelEnv, self).__init__()

    def _init_values(self):
        self.inaccuracy = 0.2

        self.range_positive_reward = 0.5
        self.bad_error = 3
        self.max_positive_reward = self.bad_error * 10
        self.bad_produced_acc = 10

        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_output_change = 3

        self.max_faktor = 0.1
        self.min_faktor = 0.04

        self.max_env_output = 15
        self.min_env_output = -self.max_env_output

        self.max_target = 10
        self.min_target = -self.max_target

        self.max_output = 1000
        self.min_output = -self.max_output

        self.max_small_target_change = 0.6
        self.max_big_target_change = abs(self.max_target) + abs(self.min_target)
        self.max_env_output_change = abs(self.max_env_output) + abs(self.min_env_output)

    def _init_physical_values(self):
        self.vel = 0
        self.last_vel = self.vel

        self.acc = 0
        self.last_acc = self.acc
        
    def _calc_physical_values(self):
        self.acc = self.faktor * self.output + self.faktor * self.env_output
        self.vel += (self.acc + self.last_acc) / 2 * self.delta_time

    def _should_reset(self):
        return abs(self.output) > 10000 or abs(self.acc) > 500 or abs(self.vel) > 500

    def _give_error(self):
        return self.target - self.vel

    def _give_measurement(self):
        return self.vel + np.random.uniform(-self.inaccuracy, self.inaccuracy)
