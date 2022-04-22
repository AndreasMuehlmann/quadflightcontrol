import gym
import pygame
import numpy as np

from pid_controller import PidController
from graph_repr import GraphRepr


def random_change(to_change, range, upper_bound, lower_bound):
    to_change += np.random.uniform(-range, range)
    to_change = lower_bound if to_change < lower_bound else to_change
    to_change = upper_bound if to_change > upper_bound else to_change
    return to_change


#TODO: delay


class PidEnv(gym.Env):
    def __init__(self):
        self.window_width = 2200
        self.window_height = 1200 

        self.total_time = 30 #in s
        self.time_available = self.total_time

        self.delta_time = 0.01

        self.fps = 500


        self.max_faktor = 0.1
        self.min_faktor = 0.01

        self.max_env_acc = 30
        self.min_env_acc = -self.max_env_acc

        self.max_target = 10
        self.min_target = -self.max_target

        self.max_output = 1000
        self.min_output = -self.max_output




        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_acc_change = 3

        self.max_small_target_change = 0.6
        self.max_big_target_change = abs(self.max_target) + abs(self.min_target)
        self.max_env_acc_change = abs(self.max_env_acc) + abs(self.min_env_acc)

        self.inaccuracy = 0.05

        self.range_positive_reward = 0.5

        self.clock = pygame.time.Clock()
        self.init_physical_values()


        self.last_small_target_change = self.time_available
        self.last_big_target_change = self.time_available
        self.last_env_acc_change = self.time_available

        self.target = np.random.uniform(self.min_target, self.max_target)
        self.faktor = np.random.uniform(self.min_faktor, self.max_faktor)
        self.env_acc = np.random.uniform(self.min_env_acc, self.max_env_acc)
        
        self.output = 0

        self.pid_controller = PidController(self.target - self.pos, self.pos, self.max_output)
        self.pid_controller.p_faktor = 0
        self.pid_controller.i_faktor = 0
        self.pid_controller.d_faktor = 0

        self.graph = 0
        self.was_reset = False

        amount_last_errors = 5
        self.last_errors = []
        for _ in range(amount_last_errors):
            self.last_errors.append(0)


        self.action_space = gym.spaces.Box(-1, 1, shape=(3,))
        self.observation_space = gym.spaces.Box(float('-inf'), float('inf'), shape=(amount_last_errors + 7,))

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

    def get_state(self):
        state = np.array([*self.last_errors, self.acc, self.vel, self.pid_controller.differentiator, self.pid_controller.integrator,\
            self.pid_controller.p_faktor, self.pid_controller.i_faktor, self.pid_controller.d_faktor])
        return state

    def step(self, action):
        self.time_available -= self.delta_time

        self.perform_action(action)

        measured_pos = self.pos + np.random.uniform(-self.inaccuracy, self.inaccuracy) 
        self.output = self.pid_controller.give_output(self.target - measured_pos, measured_pos) 
        self.calc_physical_values()

        self.target, self.last_small_target_change = self.change_val(self.target, self.last_small_target_change,
                                                                    self.time_without_small_target_change, self.max_small_target_change, self.max_target, self.min_target)
        self.target, self.last_big_target_change = self.change_val(self.target, self.last_big_target_change,
                                                                     self.time_without_big_target_change, self.max_big_target_change, self.max_target, self.min_target)
        self.env_acc, self.last_env_acc_change = self.change_val(self.env_acc, self.last_env_acc_change,
                                                                     self.time_without_env_acc_change, self.max_env_acc_change, self.max_env_acc, self.min_env_acc)

        self.last_errors.append(self.pid_controller.iir_error.outputs[-1])
        self.last_errors.pop()

        self.was_reset = False

        return self.get_state(), self.get_reward(), self.is_done(), {}

    def change_val(self, to_change_value, last_change, time_without_change, max_change,  max_val, min_val):
        if last_change - self.time_available >= time_without_change:
            to_change_value = random_change(to_change_value, max_change, max_val, min_val)
            last_change = self.time_available
        return to_change_value, last_change

    def is_done(self):
        if self.time_available <= 0:
            return True
        elif self.was_reset:
            return True
        else:
            return False

    def perform_action(self, action):
        self.pid_controller.p_faktor += action[0]
        self.pid_controller.i_faktor += action[1]
        self.pid_controller.d_faktor += action[2]

    def get_reward(self):
        if self.should_reset():
            self.was_reset = True
            self.reset()

        reward = self.get_reward_error(self.target - self.pos)
        if reward > 0:
            self.get_reward_in_positive_range(reward)

        reward -= self.get_reward_acc()

        if self.was_reset:
            reward -= self.get_reward_when_reset()

        return reward

    def should_reset(self):
        return abs(self.output) > 10000 or abs(self.acc) > 500 or abs(self.vel) > 500 or abs(self.pos) > 500

    def get_reward_error(self, error):
        return (-abs(self.target - self.pos) + self.range_positive_reward) * 100

    def get_reward_in_positive_range(self, reward):
        return (reward * 50) ** 2

    def get_reward_acc(self):
        return self.acc *10000

    def get_reward_when_reset(self):
        return 10**8 * self.time_available

    def render(self, mode='human'):
        self.clock.tick(self.fps)
        if self.graph == 0:
            self.graph = GraphRepr(2200, self.window_height)

        self.graph.add_point(self.pos)

        self.graph.target = self.target 
        self.graph.re_draw()

    def reset(self):
        self.time_available = self.total_time # in s

        self.last_small_target_change = self.time_available
        self.last_big_target_change = self.time_available
        self.last_env_acc_change = self.time_available

        self.target = np.random.uniform(self.min_target, self.max_target)
        self.faktor = np.random.uniform(self.min_faktor, self.max_faktor)
        self.env_acc = np.random.uniform(self.min_env_acc, self.max_env_acc)

        self.init_physical_values()

        self.output = 0

        self.pid_controller = PidController(self.target - self.pos, self.pos, self.max_output)
        self.pid_controller.p_faktor = 0
        self.pid_controller.i_faktor = 0
        self.pid_controller.d_faktor = 0


        if  self.graph != 0:
            self.graph = 0

        return self.get_state()