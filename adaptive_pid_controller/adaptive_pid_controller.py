from collections import deque
from copy import deepcopy

import numpy as np

import config as conf
from controller import Controller
from pid_controller import PidController
from sac import Agent


class AdaptivePidController(Controller):
    def __init__(self, p_faktor, i_faktor, d_faktor, iir_faktor, iir_order, maximum):
        self.pid_controller = PidController(p_faktor, i_faktor, d_faktor,
                                            iir_faktor, iir_order, maximum)

        self.agent = Agent(conf.input_dims, conf.n_actions, conf.chkpt_dir,
                           conf.layer_sizes, conf.batch_size, conf.action_space_high)

        self.prev_errors = [0 for _ in range(conf.amount_prev_observations)]
        self.prev_measurements = [0 for _ in range(conf.amount_prev_observations)]
        self.prev_outputs = [0 for _ in range(conf.amount_prev_observations)]

        self.observation = self._compose_observation()

    def _compose_observation(self):
        return np.array([*self.prev_errors, *self.prev_measurements, *self.prev_outputs,
                         self.pid_controller.differentiator, self.pid_controller.integrator,
                         self.pid_controller.p_faktor, self.pid_controller.i_faktor,
                         self.pid_controller.d_faktor])

    def _perform_action(self):
        self.pid_controller.p_faktor += self.action[0]
        self.pid_controller.i_faktor += self.action[1]
        self.pid_controller.d_faktor += self.action[2]

    def _update_observations(self, error, measurement, output):
        self.prev_errors.pop()
        self.prev_measurements.pop()
        self.prev_outputs.pop()
        self.prev_errors.append(error)
        self.prev_measurements.append(measurement)
        self.prev_outputs.append(output)

    def give_output(self, error, measurement):
        self.prev_observation = deepcopy(self.observation)
        self.observation = self._compose_observation()

        self.action = self.agent.choose_action(self.observation)
        self._perform_action()

        output = self.pid_controller.give_output(error, measurement)

        self._update_observations(error, measurement, output)

        return output

    def learn(self, reward, done):
        self.agent.remember(self.prev_observation, self.action, reward, self.observation, done)
        self.agent.learn()

    def load_agent_checkpoints(self):
        self.agent.load_models()


    def save_agent_models(self):
        self.agent.save_models()

    def reset(self): # this doesn't reset the agent
        self.pid_controller.reset()
        self.pid_controller.p_faktor, self.pid_controller.i_faktor, self.pid_controller.d_faktor = 0, 0, 0

        self.prev_errors = [0 for _ in range(conf.amount_prev_observations)]
        self.prev_measurements = [0 for _ in range(conf.amount_prev_observations)]
        self.prev_outputs = [0 for _ in range(conf.amount_prev_observations)]

        self.observation = self._compose_observation()
