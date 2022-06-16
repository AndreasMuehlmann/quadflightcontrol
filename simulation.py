import pygame

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

import config as conf
from vel_env import VelEnv
from pos_env import PosEnv
from pid_controller import PidController
from adaptive_pid_controller import AdaptivePidController


# TODO: mark private methods
# TODO: write documentation
# TODO: make vel_env and pos_env abstract and inherit
# TODO: make a test for the controller (if it is good enough), then also save model
# TODO: make a learning curve


def init_env():
    if conf.env == 'pos_env':
        return PosEnv()
    if conf.env == 'vel_env':
        return VelEnv()
    else:
        raise Exception(f'no env with name {conf.env} defined.')


def main():
    env = init_env()

#   controller = PidController(conf.p_faktor, conf.i_faktor, conf.d_faktor,
#                              conf.iir_faktor, conf.iir_order, conf.max_output_controller)
    controller = AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                       conf.max_output_controller)

    clock = pygame.time.Clock()
    episodes = 1000
    for episode in range(episodes):
        observation = env.reset()
        controller.reset()
        error, measurement = observation

        done = False
        while not done:
            clock.tick(conf.fps)
            output = controller.give_output(error, measurement)

            observation, reward, done, info = env.step(output)
            error, measurement = observation

            if conf.learn and type(controller) == AdaptivePidController:
                controller.learn(reward, done)

            env.render()


if __name__ == '__main__':
    main()
