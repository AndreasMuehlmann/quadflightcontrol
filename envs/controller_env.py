from collections import deque
from abc import ABCMeta, abstractmethod

import numpy as np
import gym

import config as conf
from graph_repr import GraphRepr


class ControllerEnv(gym.Env, metaclass=ABCMeta):
    @abstractmethod
    def _init_values(self):
        pass

    @abstractmethod
    def _init_physical_values(self):
        pass
        
    @abstractmethod
    def _calc_physical_values(self):
        pass

    @abstractmethod
    def _should_reset(self):
        pass

    @abstractmethod
    def _give_error(self):
        pass

    @abstractmethod
    def _give_measurement(self):
        pass

    def __init__(self):
        self._init_values()
        self._init_physical_values()

        self.delay = conf.delay

        self.window_width = conf.window_width
        self.window_height = conf.window_height

        self.total_time = conf.total_time #in s
        self.time_available = self.total_time

        self.delay = conf.delay
        self.delta_time = 1 / conf.frequency

        self.last_small_target_change = self.time_available
        self.last_big_target_change = self.time_available
        self.last_env_output_change = self.time_available

        self.target = np.random.uniform(self.min_target, self.max_target)
        self.faktor = np.random.uniform(self.min_faktor, self.max_faktor)
        self.env_output = np.random.uniform(self.min_env_output, self.max_env_output)
        
        self._init_delay_list()

        self.graph = 0
        self.was_reset = False

        self.action_space = gym.spaces.Box(-conf.action_space_high,
                                           conf.action_space_high, shape=(3,))
        self.observation_space = gym.spaces.Box(float('-inf'), float('inf'),
                                                shape=(conf.amount_prev_observations * 3 + 6,))

    def _init_delay_list(self):
        length_needed_for_delay = round(self.delay / self.delta_time + 0.5) # 0.5 for rounding up (to be sure)
        self.delay_list = deque(maxlen = length_needed_for_delay)
        for _ in range(length_needed_for_delay):
            self.delay_list.append(0)

    def step(self, new_output):
        self.time_available -= self.delta_time

        self.delay_list.append(new_output)
        self.output = self.delay_list.pop()
        self._calc_physical_values()

        self.target, self.last_small_target_change = self._change_val(self.target, self.last_small_target_change,
                                                                    self.time_without_small_target_change, self.max_small_target_change, self.max_target, self.min_target)
        self.target, self.last_big_target_change = self._change_val(self.target, self.last_big_target_change,
                                                                     self.time_without_big_target_change, self.max_big_target_change, self.max_target, self.min_target)
        self.env_output, self.last_env_output_change = self._change_val(self.env_output, self.last_env_output_change,
                                                                     self.time_without_env_output_change, self.max_env_output_change, self.max_env_output, self.min_env_output)

        self.was_reset = False

        self.measurement = self._give_measurement()
        self.error = self._give_error()
        observation = [self.error, self.measurement]

        return observation, self._get_reward(), self._is_done(), {}

    def _change_val(self, to_change_value, last_change, time_without_change, max_change,  max_val, min_val):
        if last_change - self.time_available >= time_without_change:
            to_change_value = self._random_change(to_change_value, max_change, max_val, min_val)
            last_change = self.time_available
        return to_change_value, last_change

    def _random_change(self, to_change, max_change, upper_bound, lower_bound):
        to_change += np.random.uniform(-max_change, max_change)
        to_change = lower_bound if to_change < lower_bound else to_change
        to_change = upper_bound if to_change > upper_bound else to_change
        return to_change

    def _is_done(self):
        if self.time_available <= 0:
            return True
        elif self.was_reset:
            return True
        else:
            return False

    def _get_reward(self):
        if self._should_reset():
            self.was_reset = True
            self.reset()

        produced_acc = abs(self.output * self.faktor)

        reward = abs(self.error) + self.range_positive_reward
        if reward > 0:
            reward *= self.max_positive_reward / self.range_positive_reward

        reward -= ((produced_acc / self.bad_produced_acc) ** 2 ) * self.max_positive_reward

        if self.was_reset:
            reward -= (self.bad_error + self.bad_produced_acc) *  self.time_available * 100

        return reward

    def render(self, mode='human'):
        if self.graph == 0:
            self.graph = GraphRepr(self.window_width, self.window_height)

        self.graph.add_point(self.total_time - self.time_available, self.measurement)

        self.graph.target = self.target 
        self.graph.update()

    def reset(self):
        self.time_available = self.total_time # in s

        self.last_small_target_change = self.time_available
        self.last_big_target_change = self.time_available
        self.last_env_output_change = self.time_available

        self.target = np.random.uniform(self.min_target, self.max_target)
        self.faktor = np.random.uniform(self.min_faktor, self.max_faktor)
        self.env_output = np.random.uniform(self.min_env_output, self.max_env_output)

        self._init_physical_values()
        self._init_delay_list()

        if  self.graph != 0:
            self.graph = 0

        return [self._give_error(), self._give_measurement()]
