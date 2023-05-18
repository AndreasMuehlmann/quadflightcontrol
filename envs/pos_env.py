import numpy as np

from controller_env import ControllerEnv


class PosEnv(ControllerEnv):
    def __init__(self):
        super(PosEnv, self).__init__()

    def _init_values(self):
        self.inaccuracy = 0.05

        self.range_positive_reward = 0.05
        self.bad_error = 0.2
        self.max_positive_reward = self.bad_error * 10
        self.bad_produced_acc = 5

        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_output_change = 3

        self.max_faktor = 1/50
        self.min_faktor = self.max_faktor

        self.max_env_output = 10 # strength is same as out
        self.min_env_output = -self.max_env_output

        self.max_target =  0.5 # 1
        self.min_target = -self.max_target

        self.max_output = 1000
        self.min_output = -self.max_output

        self.max_small_target_change = 0.1
        self.max_big_target_change = abs(self.max_target) + abs(self.min_target)
        self.max_env_output_change = abs(self.max_env_output) + abs(self.min_env_output)

    def _init_physical_values(self):
        self.pos = 0
        self.last_pos = self.pos

        self.vel = 0
        self.last_vel = self.vel

        self.acc = 0
        self.last_acc = self.acc
        
    def _calc_physical_values(self):
        self.acc = self.faktor * self.output + self.faktor * self.env_output
        self.vel += self.acc * self.delta_time

        self.pos += self.vel * self.delta_time + 1/2 * self.acc * self.delta_time**2
        if self.vel <= 0 and self.pos <= 0:
            self.pos = 0
            self.vel = 0

    def _should_reset(self):
        return abs(self.output) > 10000 or abs(self.acc) > 500 or \
            abs(self.vel) > 500 or abs(self.pos) > 500

    def _give_error(self):
        return self.target - self.pos

    def _give_measurement(self):
        return self.pos + np.random.uniform(-self.inaccuracy, self.inaccuracy) 
