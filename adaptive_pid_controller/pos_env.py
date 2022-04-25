from pid_controller import PidController
import numpy as np
from pid_env import PidEnv


class PosEnv(PidEnv):
    def __init__(self):
        super(PosEnv, self).__init__()

    def give_delay(self):
        return 0.05

    def give_inaccuracy(self):
        return 0.05
        
    def give_range_positive_reward(self):
        return 0.05

    def give_pid(self):
        return PidController(self.target - self.pos, self.give_measurement(), self.max_output)

    def init_max_mins(self):
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

    def give_measurement(self):
        return self.pos + np.random.uniform(-self.inaccuracy, self.inaccuracy) 

    def should_reset(self):
        return abs(self.output) > 10000 or abs(self.acc) > 500 or abs(self.vel) > 500 or abs(self.pos) > 500

    def get_reward_error(self):
        return (-abs(self.target - self.pos) + self.range_positive_reward) * 100

    def get_reward_in_positive_range(self, reward):
        return (reward * 50) ** 2

    def get_reward_acc(self):
        return self.acc *10000

    def get_reward_when_reset(self):
        return 10**8 * self.time_available