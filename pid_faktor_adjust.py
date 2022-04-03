import gym

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import numpy as np

import random
import pygame


from pid_controller import PID_Controller
from graph_repr import Graph_Repr

def random_num_p_or_n(upper_limit):
    if random.randint(0, 1) == 1:
        return random.random() * upper_limit
    return -random.random() * upper_limit

class Fly_Env(gym.Env):
    def get_state(self):
        state = np.array([*self.last_errors, self.pid_controller.differentiator, self.pid_controller.integrator,\
            self.pid_controller.p_faktor, self.pid_controller.i_faktor, self.pid_controller.d_faktor])
        return state

    def __init__(self, maximum):
        self.time_available = 15 #in s
        self.delta_time = 0.01
        self.clock = pygame.time.Clock()
        
        self.time_without_target_change = 0.4
        self.time_without_faktor_change = 0.4

        self.last_target_change = self.time_available
        self.last_faktor_change = self.time_available

        self.target_change = 0.4
        self.faktor_change = 0.05
        self.faktor = random.random()

        self.checks_per_second = 100

        self.inaccuracy = 0.05

        self.graph = 0

        self.maximum = maximum

        self.pos = 0
        self.last_pos = self.pos

        self.vel = 0
        self.last_vel = self.vel

        self.acc = 0
        self.last_acc = 0

        self.target = random_num_p_or_n(self.target_change) * 2
        self.on_target_start = None

        self.pid_controller = PID_Controller(self.target - self.pos, self.pos, self.maximum)
        self.pid_controller.p_faktor = 0
        self.pid_controller.i_faktor = 0
        self.pid_controller.d_faktor = 0

        amount_last_errors = 50 
        self.last_errors = []
        for _ in range(amount_last_errors):
            self.last_errors.append(0)

        self.action_space = gym.spaces.Discrete(7)
        self.observation_space = gym.spaces.Box(float('-inf'), float('inf'), shape=(amount_last_errors + 5,))


    def step(self, action):
        self.time_available -= self.delta_time

        if action == 1:
            self.pid_controller.p_faktor += 1

        elif action == 2:
            self.pid_controller.p_faktor -= 1

        elif action == 3:
            self.pid_controller.i_faktor += 1

        elif action == 4:
            self.pid_controller.i_faktor -= 1

        elif action == 5:
            self.pid_controller.d_faktor += 1

        elif action == 6:
            self.pid_controller.d_faktor -= 1

        measured_pos = self.pos + random_num_p_or_n(self.inaccuracy) 
        rpm = self.pid_controller.give_rpm(self.target - measured_pos, measured_pos) 
        if abs(rpm) > 1000:
            self.reset()

        self.acc = self.faktor * rpm
        if abs(self.acc) > 100:
            self.reset()

        self.vel += (self.acc + self.last_acc) / 2 * self.delta_time
        if abs(self.vel) > 100:
            self.reset()

        self.pos += (self.vel + self.last_vel) / 2 * self.delta_time
        if abs(self.pos) > 1000:
            self.reset()


        reward = ((-abs(self.target - self.pos) + 0.03) * 10) ** 3
        if reward > 0:
            if self.on_target_start is None:
                self.on_target_start = self.time_available

            reward ** (1 + self.on_target_start - self.time_available)
        else:
            self.on_target_start = None

        reward -= (self.acc * 0.01) ** 2

        if self.time_available <= 0:
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

        return self.get_state(), reward, done, info

    def render(self, mode='human'):
        self.clock.tick(self.checks_per_second)
        if self.graph == 0:
            self.graph = Graph_Repr(1600, 1000)

        self.graph.add_point(self.pos)

        self.graph.target = self.target 
        self.graph.re_draw()

        print(f'p: {self.pid_controller.p_faktor}, i: {self.pid_controller.i_faktor}, d: {self.pid_controller.d_faktor}')


    def reset(self):
        self.pos = 0
        self.last_pos = 0

        self.vel = 0
        self.last_vel = 0

        self.acc = 0
        self.last_acc = 0

        random_number = random_num_p_or_n(self.faktor_change) * 2
        if self.faktor + random_number <= 0:
            self.faktor -= random_number

        self.target = random_num_p_or_n(self.target_change)
        self.on_target_start = None

        self.time_available = 15 # in s

        self.pid_controller = PID_Controller(self.target - self.pos, self.pos, self.maximum)

        self.last_target_change = self.time_available
        self.last_faktor_change = self.time_available

        if  self.graph != 0:
            self.graph = 0

        self.pid_controller.p_faktor = 0
        self.pid_controller.i_faktor = 0
        self.pid_controller.d_faktor = 0

        return self.get_state()


def build_model(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape=(1,states)))
    model.add(Dense(24, activation = 'relu'))
    model.add(Dense(24, activation = 'relu'))
    model.add(Dense(actions, activation = 'linear'))
    return model

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit = 50000, window_length = 1)
    dqn = DQNAgent(model = model, memory = memory, policy = policy,
        nb_actions = actions, nb_steps_warmup = 10, target_model_update = 1e-2)
    return dqn

env = Fly_Env(6000)
states = env.observation_space.shape[0]
actions = env.action_space.n

model = build_model(states, actions)
model.summary()

dqn = build_agent(model, actions)
dqn.compile(Adam(lr = 1e-3), metrics=['mae'])
dqn.fit(env, nb_steps = 1000000, visualize = False, verbose = 1)
input('ready?')

_ = dqn.test(env, nb_episodes=15, visualize=True)