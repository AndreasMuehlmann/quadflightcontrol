import os

import pygame
import numpy as np

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

import config as conf
from init_env import init_env
from adaptive_pid_controller import AdaptivePidController
from run_episode import run_episode
from plotting import plot_learning_curve


# TODO: low priority: competition is inconsistent (maybe something wrong with saving or loading)
# TODO: low priority: maybe look up a better way for competition
# TODO: low priority: pygame window moves to top left


class Training():
    def __init__(self):
        self.env = init_env()
        self.controller = AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                    conf.max_output_controller)
        if conf.load_checkpoint:
            self.controller.load_agent_checkpoints()
        self.controller.save_agent_models()

        self.figure_file = self._give_figure_file_path()

        self.competition_score_history = []
        self.last_episode_with_competition = 0

        self.clock = pygame.time.Clock()

    def _give_figure_file_path(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.figure_file_name = f'learning_curve_{conf.env}.png'
        return os.path.join(self.dir_path, 'adaptive_pid_controller','plots', self.figure_file_name)

    def train(self):
        for episode in range(conf.episodes):
            score = run_episode(self.env, self.controller, conf.learn)
            print(f'episode: {episode}, score: {round(score, 2)}')

            if _should_compete():
                self.last_episode_with_competition = episode

                if self._is_current_controller_better_than_saved():
                    self.controller.save_agent_models()
                    print('\n\n')

        if conf.learn:
            x_axis = [x + 1 for x in range(conf.episodes)]
            plot_learning_curve(x_axis, self.competition_score_history, self.figure_file)

    def _should_compete(self):
        return conf.learn and episode - self.last_episode_with_competition  >= conf.episodes_before_competing

    def _is_current_controller_better_than_saved(self):
        print('----------COMPETING----------\n')
        print('current agent')

        avg_current_controller = self._avg_over_episodes(self.controller)
        print(f'average {conf.count_episodes_avg_over_for_competing} episodes: '\
              + f' {avg_current_controller}\n\n')

        print('prev agent')

        prev_best_controller = AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                    conf.max_output)
        prev_best_controller.load_agent_checkpoints()

        avg_prev_best_controller = self._avg_over_episodes(prev_best_controller)
        self.competition_score_history.append(avg_prev_best_controller)

        print(f'average {conf.count_episodes_avg_over_for_competing} episodes: '\
              + f' {avg_prev_best_controller}')
        print('\n----------END OF COMPETING--------')

        return avg_current_controller > avg_prev_best_controller

    def _avg_over_episodes(self, controller):
        scores = []
        for episode in range(conf.count_episodes_avg_over_for_competing):
            score = run_episode(self.env, controller, False)
            print(f'episode: {episode}, score: {score}')
            scores.append(score)
        return np.mean(scores)


if __name__ == '__main__':
    training = Training()
    training.train()
