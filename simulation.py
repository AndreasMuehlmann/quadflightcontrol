import pygame

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

import config as conf
from vel_env import VelEnv
from pos_env import PosEnv
from pid_controller import PidController
from adaptive_pid_controller import AdaptivePidController


# TODO: adaptive_pid_controller has to be trainable
# TODO: mark private methods
# TODO: write documentation
# TODO: make vel_env and pos_env abstract and inherit
# TODO: make a test for the controller (if it is good enough)
# TODO: make a learning curve
# TODO: reset the controller after every episode


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
        error, measurement = observation

        done = False
        while not done:
            clock.tick(conf.fps)
            output = controller.give_output(error, measurement)
            print(f'p: {controller.pid_controller.p_faktor}, i: {controller.pid_controller.i_faktor}, d: {controller.pid_controller.d_faktor}')

            prev_observation = observation
            observation, reward, done, info = env.step(output)
            error, measurement = observation
            controller.learn(reward, done)

            env.render()


if __name__ == '__main__':
    main()
