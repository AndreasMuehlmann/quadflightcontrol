import gym
import random
import pygame
import numpy as np

from pid_controller import PID_Controller
from graph_repr import Graph_Repr


def random_num_p_or_n(upper_limit):
    if random.randint(0, 1) == 1:
        return random.random() * upper_limit
    return -random.random() * upper_limit


class Fly_Env(gym.Env):
    def __init__(self, maximum):
        self.time_available = 30 #in s
        self.delta_time = 0.01
        self.clock = pygame.time.Clock()
        
        self.time_without_target_change = 0.8
        self.time_without_faktor_change = 0.5

        self.last_target_change = self.time_available
        self.last_faktor_change = self.time_available

        self.target_change = 0.6
        self.faktor_change = 0.0
        self.faktor = random.random()

        self.checks_per_second = 500

        self.inaccuracy = 0.05

        self.graph = 0

        self.maximum = maximum

        self.pos = 0
        self.last_pos = self.pos

        self.vel = 0
        self.last_vel = self.vel

        self.acc = 0
        self.last_acc = 0
        
        self.rpm = 0

        random_number = random_num_p_or_n(self.target_change)
        self.target = (random_number / abs(random_number)) * self.target_change * 5
        self.on_target_start = None

        self.pid_controller = PID_Controller(self.target - self.pos, self.pos, self.maximum)
        self.pid_controller.p_faktor = 0
        self.pid_controller.i_faktor = 0
        self.pid_controller.d_faktor = 0

        amount_last_errors = 5
        self.last_errors = []
        for _ in range(amount_last_errors):
            self.last_errors.append(0)

        self.action_space = gym.spaces.Box(-1, 1, shape=(3,))
        self.observation_space = gym.spaces.Box(float('-inf'), float('inf'), shape=(amount_last_errors + 7,))

        self.was_reset = False

    def get_state(self):
        state = np.array([*self.last_errors, self.acc, self.vel, self.pid_controller.differentiator, self.pid_controller.integrator,\
            self.pid_controller.p_faktor, self.pid_controller.i_faktor, self.pid_controller.d_faktor])
        return state

    def step(self, action):
        self.perform_action(action)

        measured_pos = self.pos + random_num_p_or_n(self.inaccuracy) 
        self.rpm = self.pid_controller.give_rpm(self.target - measured_pos, measured_pos) 
        self.acc = self.faktor * self.rpm
        self.vel += (self.acc + self.last_acc) / 2 * self.delta_time
        self.pos += (self.vel + self.last_vel) / 2 * self.delta_time

        reward = self.get_reward()

        self.time_available -= self.delta_time
        if self.time_available <= 0:
            done = True
        elif self.was_reset:
            done = True
        else:
            done = False
        

        if self.last_faktor_change - self.time_available >= self.time_without_faktor_change:
            random_number = random_num_p_or_n(self.faktor_change)
            if self.faktor + random_number <= 0:
                self.faktor -= random_number
            self.last_faktor_change = self.time_available

        if self.last_target_change - self.time_available >= self.time_without_target_change:
            self.target += random_num_p_or_n(self.target_change)
            self.last_target_change = self.time_available

        info = {}

        self.last_errors.append(self.pid_controller.iir_error.outputs[-1])
        self.last_errors.pop()

        self.was_reset = False

        return self.get_state(), reward, done, info

    def perform_action(self, action):
            self.pid_controller.p_faktor += action[0]
            self.pid_controller.i_faktor += action[1]
            self.pid_controller.d_faktor += action[2]

    def get_reward(self):
        if abs(self.rpm) > 10000 or abs(self.acc) > 500 or abs(self.vel) > 500 or abs(self.pos) > 500:
            self.was_reset = True
            self.reset()

        reward = (-abs(self.target - self.pos) + 0.05) * 1000
        if reward > 0:
            reward *= 50
            reward **= 2

            cap = 0.5
            faktor = 0.1
            if self.time_available * faktor > cap:
                 reward /= self.time_available * faktor
            else:
                reward /= cap

        reward -= self.acc *1000

        if self.was_reset:
            reward -= 10**7 * self.time_available

        return reward

    def render(self, mode='human'):
        self.clock.tick(self.checks_per_second)
        if self.graph == 0:
            self.graph = Graph_Repr(2200, 1200)

        self.graph.add_point(self.pos)

        self.graph.target = self.target 
        self.graph.re_draw()

    def reset(self):
        self.pos = 0
        self.last_pos = 0

        self.vel = 0
        self.last_vel = 0

        self.acc = 0
        self.last_acc = 0

        self.rpm = 0

        random_number = random_num_p_or_n(self.faktor_change)
        if self.faktor + random_number <= 0:
            self.faktor -= random_number
        else:
            self.faktor += random_number

        random_number = random_num_p_or_n(self.target_change)
        self.target = (random_number / abs(random_number)) * self.target_change * 5
        self.on_target_start = None

        self.time_available = 30 # in s

        self.pid_controller = PID_Controller(self.target - self.pos, self.pos, self.maximum)

        self.last_target_change = self.time_available
        self.last_faktor_change = self.time_available

        if  self.graph != 0:
            self.graph = 0

        self.pid_controller.p_faktor = 0
        self.pid_controller.i_faktor = 0
        self.pid_controller.d_faktor = 0

        return self.get_state()