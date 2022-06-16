import os

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
# TODO: make a test for the controller (if it is good enough), then also save model
# TODO: anstatt of init_function make dict
# TODO: display the plot while it is running


def init_env():
    if conf.env == 'pos_env':
        return PosEnv()
    if conf.env == 'vel_env':
        return VelEnv()
    else:
        raise Exception(f'no env with name {conf.env} defined.')


def init_controller():
    if conf.controller == 'pid_controller':
        return PidController(conf.p_faktor, conf.i_faktor, conf.d_faktor,
                             conf.iir_faktor, conf.iir_order, conf.max_output_controller)
    if conf.controller == 'adaptive_pid_controller':
        return AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                     conf.max_output_controller)
    else:
        raise Exception(f'no controller with name {conf.env} defined.')


def main():
    env = init_env()
    controller = init_controller()

    score_history = []
    best_score = float('-inf')

    dir_path = os.path.dirname(os.path.abspath(__file__))
    figure_file_name = f'learning_curve_{conf.env}.png'
    figure_file = os.path.join(dir_path, 'adaptive_pid_controller','plots', figure_file_name)

    clock = pygame.time.Clock()

    init_changing_plot()

    for episode in range(conf.episodes):
        observation = env.reset()
        error, measurement = observation

        controller.reset()

        score = 0
        done = False
        while not done:
            clock.tick(conf.fps)

            output = controller.give_output(error, measurement)

            observation, reward, done, info = env.step(output)
            error, measurement = observation
            score += reward
            env.render()

            if conf.learn and type(controller) == AdaptivePidController:
                controller.learn(reward, done)

        score_history.append(score)
        avg_score = np.mean(score_history[-conf.range_avg:])

        if score > best_score:
            best_score = score
            if conf.save_model and conf.learn and type(controller) == AdaptivePidController:
                controller.save_models()

        draw_plot(episode, score_history)
        print(f'episode: {episode}, score {round(score, 2)}, avg_score {round(avg_score, 2)}')

    if learn and save_model:
        x = [i+1 for i in range(episodes)]
        plot_learning_curve(x, score_history, figure_file)



if __name__ == '__main__':
    main()
