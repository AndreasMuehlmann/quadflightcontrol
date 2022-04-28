import numpy as np
from pid_env import PidEnv


class PosEnv(PidEnv):
    def __init__(self):
        super(PosEnv, self).__init__()

    def init_values(self):
        self.delay = 0.05
        self.inaccuracy = 0.05

        self.range_positive_reward = 0.05

        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_acc_change = 3

        self.max_faktor = 0.1
        self.min_faktor = 0.01

        self.max_env_acc = 30
        self.min_env_acc = -self.max_env_acc

        self.max_target =  1
        self.min_target = -self.max_target

        self.max_output = 1000
        self.min_output = -self.max_output

        self.max_small_target_change = 0.1
        self.max_big_target_change = abs(self.max_target) + abs(self.min_target)
        self.max_env_acc_change = abs(self.max_env_acc) + abs(self.min_env_acc)

    def init_physical_values(self):
        self.pos = 0
        self.last_pos = self.pos

        self.vel = 0
        self.last_vel = self.vel

        self.acc = 0
        self.last_acc = self.acc
        
    def calc_physical_values(self):
        self.acc = self.faktor * self.output + self.env_acc
        self.vel += (self.acc + self.last_acc) / 2 * self.delta_time
        self.pos += (self.vel + self.last_vel) / 2 * self.delta_time

    def should_reset(self):
        return abs(self.output) > 10000 or abs(self.acc) > 500 or abs(self.vel) > 500 or abs(self.pos) > 500

    def give_error(self):
        return self.target - self.pos

    def give_measurement(self):
        return self.pos + np.random.uniform(-self.inaccuracy, self.inaccuracy) 