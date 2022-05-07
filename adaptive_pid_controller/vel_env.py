from pid_env import PidEnv
import numpy as np


class VelEnv(PidEnv):
    def __init__(self):
        super(VelEnv, self).__init__()

    def init_values(self):
        self.delay = 0.05

        self.inaccuracy = 0.2
        self.iir_faktor = 0.85
        self.iir_order = 5

        self.range_positive_reward = 0.5
        self.bad_error = 3
        self.bad_produced_acc = 10

        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_force_change = 3

        self.max_faktor = 0.1
        self.min_faktor = 0.04

        self.max_env_force = 15
        self.min_env_force = -self.max_env_force

        self.max_target = 10
        self.min_target = -self.max_target

        self.max_output = 1000
        self.min_output = -self.max_output

        self.max_small_target_change = 0.6
        self.max_big_target_change = abs(self.max_target) + abs(self.min_target)
        self.max_env_force_change = abs(self.max_env_force) + abs(self.min_env_force)

    def init_physical_values(self):
        self.measured_vel = 0

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