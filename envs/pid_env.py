import sys
import os
import gym
import pygame
from collections import deque
import numpy as np
from abc import ABCMeta, abstractmethod

current_dir = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current_dir)
child_parent = os.path.join(parent, 'pid_controller')
sys.path.append(child_parent)
from pid_controller import PidController

from graph_repr import GraphRepr


def random_change(to_change, range, upper_bound, lower_bound):
    to_change += np.random.uniform(-range, range)
    to_change = lower_bound if to_change < lower_bound else to_change
    to_change = upper_bound if to_change > upper_bound else to_change
    return to_change


class PidEnv(gym.Env, metaclass=ABCMeta):
    @abstractmethod
    def init_values(self):
        pass

    @abstractmethod
    def init_physical_values(self):
        pass
        
    @abstractmethod
    def calc_physical_values(self):
        pass

    @abstractmethod
    def should_reset(self):
        pass

    @abstractmethod
    def give_error(self):
        pass

    @abstractmethod
    def give_measurement(self):
        pass

    def __init__(self):
        self.init_values()
        self.init_physical_values()

        self.window_width = 1200
        self.window_height = 800 

        self.total_time = 30 #in s
        self.time_available = self.total_time

        self.delta_time = 0.05

        self.fps = 1  / self.delta_time

        self.clock = pygame.time.Clock()

        self.last_small_target_change = self.time_available
        self.last_big_target_change = self.time_available
        self.last_env_force_change = self.time_available

        self.target = np.random.uniform(self.min_target, self.max_target)
        self.faktor = np.random.uniform(self.min_faktor, self.max_faktor)
        self.env_force = np.random.uniform(self.min_env_force, self.max_env_force)
        
        self.output = 0
        self.init_prev_outputs()

        self.measurement = self.give_measurement()

        self.pid_controller = PidController(0, 0, 0,self.iir_faktor, self.iir_order, self.max_output)

        self.graph = 0
        self.was_reset = False
        self.max_positive_reward = self.bad_error * 10

        self.amount_prev_errors = int(2 / self.delta_time)
        self.init_prev_errors()

        self.action_space = gym.spaces.Box(-1, 1, shape=(3,))
        self.observation_space = gym.spaces.Box(float('-inf'), float('inf'), shape=(self.amount_prev_errors + 6,))

    def init_prev_outputs(self):
        self.prev_outputs = deque(maxlen = round(self.fps * self.delay + 0.5))
        for _ in range(round(self.fps * self.delay + 0.5)):
            self.prev_outputs.append(0)

    def init_prev_errors(self):
        self.prev_errors = []
        for _ in range(self.amount_prev_errors):
            self.prev_errors.append(0)

    def get_state(self):
        state = np.array([*self.prev_errors, self.output, self.pid_controller.differentiator, self.pid_controller.integrator,\
            self.pid_controller.p_faktor, self.pid_controller.i_faktor, self.pid_controller.d_faktor])
        return state

    def step(self, action):
        self.time_available -= self.delta_time

        self.perform_action(action)

        self.measurement = self.give_measurement()
        self.prev_outputs.append(self.pid_controller.give_output(self.target - self.measurement, self.measurement))

        self.output = self.prev_outputs.pop()
        self.calc_physical_values()

        self.target, self.last_small_target_change = self.change_val(self.target, self.last_small_target_change,
                                                                    self.time_without_small_target_change, self.max_small_target_change, self.max_target, self.min_target)
        self.target, self.last_big_target_change = self.change_val(self.target, self.last_big_target_change,
                                                                     self.time_without_big_target_change, self.max_big_target_change, self.max_target, self.min_target)
        self.env_force, self.last_env_force_change = self.change_val(self.env_force, self.last_env_force_change,
                                                                     self.time_without_env_force_change, self.max_env_force_change, self.max_env_force, self.min_env_force)

        self.prev_errors.append(self.pid_controller.iir_error.outputs[-1])
        self.prev_errors.pop()

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

        produced_acc = abs(self.output * self.faktor)

        reward = abs(self.give_error()) + self.range_positive_reward
        if reward > 0:
            reward *= self.max_positive_reward / self.range_positive_reward

        reward -= ((produced_acc / self.bad_produced_acc) ** 2 ) * self.max_positive_reward

        if self.pid_controller.integrator >= self.max_output:
            reward -= self.bad_produced_acc * 1000

        if self.was_reset:
            reward -= (self.bad_error + self.bad_produced_acc) *  self.time_available * 100

        return reward

    def render(self, mode='human'):
        self.clock.tick(self.fps)
        if self.graph == 0:
            self.graph = GraphRepr(self.window_width, self.window_height)

        self.graph.add_point(self.total_time - self.time_available, self.measurement)

        self.graph.target = self.target 
        self.graph.re_draw()

    def reset(self):
        self.time_available = self.total_time # in s

        self.last_small_target_change = self.time_available
        self.last_big_target_change = self.time_available
        self.last_env_force_change = self.time_available

        self.target = np.random.uniform(self.min_target, self.max_target)
        self.faktor = np.random.uniform(self.min_faktor, self.max_faktor)
        self.env_force = np.random.uniform(self.min_env_force, self.max_env_force)

        self.init_physical_values()

        self.output = 0
        self.init_prev_outputs()

        self.pid_controller = PidController(0, 0, 0, self.iir_faktor, self.iir_order, self.max_output)

        if  self.graph != 0:
            self.graph = 0

        self.init_prev_errors()

        return self.get_state()
