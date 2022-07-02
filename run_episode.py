import pygame

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

import config as conf
from init_controller import init_controller
from init_env import init_env
from adaptive_pid_controller import AdaptivePidController


def run_episode(env, controller, learn=False):
    clock = pygame.time.Clock()

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

        if learn and type(controller) == AdaptivePidController:
            controller.learn(reward, done)

    return score


if __name__ == '__main__':
    controller = init_controller()
    if type(controller) == AdaptivePidController:
        controller.load_agent_checkpoints()
    score = run_episode(init_env(), init_controller())
    print(score)
