import numpy as np

import config as conf
from pid_env import PidEnv


class VelEnv(PidEnv):
    def __init__(self):
        super(VelEnv, self).__init__()

    def init_values(self):
        self.inaccuracy = conf.vel_env_inaccuracy

        self.range_positive_reward = conf.vel_env_range_positive_reward
        self.bad_error = conf.vel_env_bad_error
        self.bad_produced_acc = conf.vel_env_bad_produced_acc


        self.time_without_small_target_change = conf.vel_env_time_without_small_target_change
        self.time_without_big_target_change = conf.vel_env_time_without_big_target_change
        self.time_without_env_force_change = conf.vel_env_time_without_env_force_change

        self.max_faktor = conf.vel_env_max_faktor
        self.min_faktor = conf.vel_env_min_faktor

        self.max_env_force = conf.vel_env_max_env_force # strength is same as output
        self.min_env_force = conf.vel_env_min_env_force

        self.max_target =  conf.vel_env_max_target
        self.min_target = conf.vel_env_min_target

        self.max_output = conf.vel_env_max_output
        self.min_output = conf.vel_env_min_output

        self.max_small_target_change = conf.vel_env_max_small_target_change
        self.max_big_target_change = conf.vel_env_max_big_target_change
        self.max_env_force_change = conf.vel_env_max_env_force_change

    def init_physical_values(self):
        self.vel = 0
        self.last_vel = self.vel

        self.acc = 0
        self.last_acc = self.acc
        
    def calc_physical_values(self):
        self.acc = self.faktor * self.output + self.faktor * self.env_force
        self.vel += (self.acc + self.last_acc) / 2 * self.delta_time

    def should_reset(self):
        return abs(self.output) > 10000 or abs(self.acc) > 500 or abs(self.vel) > 500

    def give_error(self):
        return self.target - self.vel

    def give_measurement(self):
        return self.vel + np.random.uniform(-self.inaccuracy, self.inaccuracy)
