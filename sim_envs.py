import os
import time

import pygame
import numpy as np

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

import config as conf
from vel_env import VelEnv
from pos_env import PosEnv
from pid_controller import PidController
from adaptive_pid_controller import AdaptivePidController
from plotting import init_changing_plot, draw_plot, plot_learning_curve


# TODO: mark private methods
# TODO: write documentation
# TODO: make vel_env and pos_env abstract and inherit
# TODO: make a test for the controller (the last saved model competes against current)
# TODO: anstatt of init_function make dict
# TODO: display the plot while it is running also in this venv (maybe dependencie missing)


class SimEnv():
    def __init__(self):
        self.env = self.init_env()
        self.controller = self.init_controller()

        self.score_history = []
        self.best_score = float('-inf')

        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.figure_file_name = f'learning_curve_{conf.env}.png'
        self.figure_file = os.path.join(self.dir_path, 'adaptive_pid_controller','plots', self.figure_file_name)

        self.clock = pygame.time.Clock()

        init_changing_plot()

        self.last_episode_with_competition = 0

    def init_env(self):
        if conf.env == 'pos_env':
            return PosEnv()
        if conf.env == 'vel_env':
            return VelEnv()
        else:
            raise Exception(f'no env with name {conf.env} defined.')


    def init_controller(self):
        if conf.controller == 'pid_controller':
            return PidController(conf.p_faktor, conf.i_faktor, conf.d_faktor,
                                conf.iir_faktor, conf.iir_order, conf.max_output_controller)
        if conf.controller == 'adaptive_pid_controller':
            return AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                        conf.max_output_controller)
        else:
            raise Exception(f'no controller with name {conf.env} defined.')

    def run(self):
        for episode in range(conf.episodes):
            observation = self.env.reset()
            self.error, self.measurement = observation

            self.controller.reset()

            score = self.run_episode(self.controller, conf.learn)
            self.score_history.append(score)
            avg_score = np.mean(self.score_history[-conf.range_avg:])

            draw_plot(episode, self.score_history)
            print(f'episode: {episode}, score {round(score, 2)}, avg_score {round(avg_score, 2)}')

            if conf.save_model and conf.learn and type(self.controller) == AdaptivePidController:
                if episode - self.last_episode_with_competition  >= 3 and \
                   self.is_current_controller_better_than_saved():
                    self.last_episode_with_competition = episode
                    self.controller.save_agent_models()

        if conf.learn and conf.save_model:
            x = [i+1 for i in range(conf.episodes)]
            plot_learning_curve(x, self.score_history, self.figure_file)

    def run_episode(self, controller, learn):
        score = 0
        done = False
        while not done:
            self.clock.tick(conf.fps)
            time.sleep(conf.delta_time)


            output = controller.give_output(self.error, self.measurement)

            observation, reward, done, info = self.env.step(output)
            self.error, self.measurement = observation
            score += reward
            self.env.render()

            if learn and type(controller) == AdaptivePidController:
                controller.learn(reward, done)
        return score

    def is_current_controller_better_than_saved(self):
        print('...current agent...')
        avg_current_controller = self.avg_over_episodes(self.controller)
        print(f'average {conf.count_episodes_avg_over_for_competing} episodes: '\
              + f' {avg_current_controller}')

        prev_best_controller = self.init_controller()
        print('...prev agent...')
        avg_prev_best_controller = self.avg_over_episodes(prev_best_controller)
        print(f'average {conf.count_episodes_avg_over_for_competing} episodes: '\
              + f' {avg_prev_best_controller}')
        return avg_current_controller > avg_prev_best_controller

    def avg_over_episodes(self, controller):
        scores = []
        for episode in range(conf.count_episodes_avg_over_for_competing):
            score = self.run_episode(controller, True)
            print(f'episode: {episode}, score: {score}')
            scores.append(score)
        return np.mean(scores)


if __name__ == '__main__':
    sim_env = SimEnv()
    sim_env.run()
