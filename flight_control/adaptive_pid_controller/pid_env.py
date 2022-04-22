import gym
import pygame
import numpy as np
from abc import ABCMeta, abstractmethod

from graph_repr import GraphRepr


def random_change(to_change, range, upper_bound, lower_bound):
    to_change += np.random.uniform(-range, range)
    to_change = lower_bound if to_change < lower_bound else to_change
    to_change = upper_bound if to_change > upper_bound else to_change
    return to_change


#TODO: delay


class PidEnv(gym.Env, metaclass=ABCMeta):
    def __init__(self):
        self.window_width = 2200
        self.window_height = 1200 

        self.total_time = 30 #in s
        self.time_available = self.total_time

        self.delta_time = 0.01

        self.fps = 500

        #maybe into subclasses
        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_acc_change = 3


        self.clock = pygame.time.Clock()

        self.inaccuracy = self.give_inaccuracy()
        self.range_positive_reward = self.give_range_positive_reward() 
        self.init_physical_values()
        self.init_max_mins()

        self.last_small_target_change = self.time_available
        self.last_big_target_change = self.time_available
        self.last_env_acc_change = self.time_available

        self.target = np.random.uniform(self.min_target, self.max_target)
        self.faktor = np.random.uniform(self.min_faktor, self.max_faktor)
        self.env_acc = np.random.uniform(self.min_env_acc, self.max_env_acc)
        
        self.output = 0

        self.pid_controller = self.give_pid()
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

    @abstractmethod
    def give_pid(self):
        pass

    @abstractmethod
    def give_delay(self):
        pass

    @abstractmethod
    def give_inaccuracy(self):
        pass
        
    @abstractmethod
    def give_range_positive_reward(self):
        pass

    @abstractmethod
    def init_max_mins(self):
        pass

    @abstractmethod
    def init_physical_values(self):
        pass
        
    @abstractmethod
    def calc_physical_values(self):
        pass

    def get_state(self):
        state = np.array([*self.last_errors, self.acc, self.vel, self.pid_controller.differentiator, self.pid_controller.integrator,\
            self.pid_controller.p_faktor, self.pid_controller.i_faktor, self.pid_controller.d_faktor])
        return state

    def step(self, action):
        self.time_available -= self.delta_time

        self.perform_action(action)

        self.measurement = self.give_measurement()
        self.output = self.pid_controller.give_output(self.target - self.measurement, self.measurement) 
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

    @abstractmethod
    def give_measurement(self):
        pass

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

        reward = self.get_reward_error()
        if reward > 0:
            self.get_reward_in_positive_range(reward)

        reward -= self.get_reward_acc()

        if self.was_reset:
            reward -= self.get_reward_when_reset()

        return reward

    @abstractmethod
    def should_reset(self):
        pass

    @abstractmethod
    def get_reward_error(self, error):
        pass

    @abstractmethod
    def get_reward_in_positive_range(self, reward):
        pass

    @abstractmethod
    def get_reward_acc(self):
        pass

    @abstractmethod
    def get_reward_when_reset(self):
        pass

    def render(self, mode='human'):
        self.clock.tick(self.fps)
        if self.graph == 0:
            self.graph = GraphRepr(self.window_width, self.window_height)

        self.graph.add_point(self.measurement)

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

        self.pid_controller = self.give_pid()
        self.pid_controller.p_faktor = 0
        self.pid_controller.i_faktor = 0
        self.pid_controller.d_faktor = 0


        if  self.graph != 0:
            self.graph = 0

        return self.get_state()