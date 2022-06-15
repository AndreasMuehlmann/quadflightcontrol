from collections import deque

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

    def compose_input_agent(self):
        return np.array([*self.prev_errors, *self.prev_measurements, *self.prev_outputs,
                         self.pid_controller.differentiator, self.pid_controller.integrator,
                         self.pid_controller.p_faktor, self.pid_controller.i_faktor,
                         self.pid_controller.d_faktor])

    def perform_action(self, action):
        self.pid_controller.p_faktor += action[0]
        self.pid_controller.p_faktor += action[1]
        self.pid_controller.p_faktor += action[2]

    def update_observations(self, error, measurement, output):
        self.prev_errors.pop()
        self.prev_measurements.pop()
        self.prev_outputs.pop()
        self.prev_errors.append(error)
        self.prev_measurements.append(measurement)
        self.prev_outputs.append(output)

    def give_output(self, error, measurement):
        action = self.agent.choose_action(self.compose_input_agent())
        self.perform_action(action)

        output = self.pid_controller.give_output(error, measurement)

        self.update_observations(error, measurement, output)

        return output
