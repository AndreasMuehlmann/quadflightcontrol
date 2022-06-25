import os

import pygame
import numpy as np

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

import config as conf
from init_controller import init_controller
from init_env import init_env
from adaptive_pid_controller import AdaptivePidController
from run_episode import run_episode
from plotting import init_changing_plot, draw_plot, plot_learning_curve


# TODO: mark private methods
# TODO: write documentation
# TODO: display the plot while it is running also in this venv (maybe dependencie missing)
# TODO: make pygame not print and init
# TODO: competition is inconsistent (maybe longer and load also current agent)
# TODO: pygame window moves to top left


class Training():
    def __init__(self):
        self.env = init_env()
        self.controller = AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                    conf.max_output_controller)
        if conf.load_checkpoint:
            self.controller.load_agent_checkpoints()
        self.controller.save_agent_models()

        self.score_history_saved_agent_competition = []

        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.figure_file_name = f'learning_curve_{conf.env}.png'
        self.figure_file = os.path.join(self.dir_path, 'adaptive_pid_controller','plots', self.figure_file_name)

        self.clock = pygame.time.Clock()

        init_changing_plot()

        self.last_episode_with_competition = 0

    def train(self):
        for episode in range(conf.episodes):
            score = run_episode(self.env, self.controller, conf.learn)

            print(f'episode: {episode}, score: {round(score, 2)}')

            if conf.learn and episode - self.last_episode_with_competition  >= conf.episodes_before_competing:
                self.last_episode_with_competition = episode

                if self.is_current_controller_better_than_saved():
                    self.controller.save_agent_models()
                    print('\n\n')
                    draw_plot(episode // conf.episodes_before_competing, self.score_history_saved_agent_competition)

        if conf.learn:
            x = [i+1 for i in range(conf.episodes)]
            plot_learning_curve(x, self.score_history, self.figure_file)

    def is_current_controller_better_than_saved(self):
        print('----------COMPETING----------\n')
        print('current agent')
        avg_current_controller = self.avg_over_episodes(self.controller)
        print(f'average {conf.count_episodes_avg_over_for_competing} episodes: '\
              + f' {avg_current_controller}')

        print('\n')
        prev_best_controller = init_controller()
        prev_best_controller.load_agent_checkpoints()
        print('prev agent')
        avg_prev_best_controller = self.avg_over_episodes(prev_best_controller)
        self.score_history_saved_agent_competition.append(avg_prev_best_controller)
        print(f'average {conf.count_episodes_avg_over_for_competing} episodes: '\
              + f' {avg_prev_best_controller}')

        print('\n----------END OF COMPETING--------')
        return avg_current_controller > avg_prev_best_controller

    def avg_over_episodes(self, controller):
        scores = []
        for episode in range(conf.count_episodes_avg_over_for_competing):
            score = run_episode(self.env, controller, False)
            print(f'episode: {episode}, score: {score}')
            scores.append(score)
        return np.mean(scores)


if __name__ == '__main__':
    training = Training()
    training.train()
