import pygame

import config as conf
from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from vel_env import VelEnv
from pos_env import PosEnv
from pid_controller import PidController
from adaptive_pid_controller import AdaptivePidController


# TODO: something wrong in vel_env
# TODO: chkpt_dir, iir_faktor, iir_order should change with env changing
# TODO: adaptive_pid_controller has to be trainable
# TODO: prev observation stuff in pid_env not sure
# TODO: put action_space_high in pid_env
# TODO: rename pid_env to controller_env
# TODO: pid_controller has to inherit from controller


def main():
    env = PosEnv()

    if type(env) == PosEnv:
        env_kind = 'pos_env'
    elif type(env) == VelEnv:
        env_kind = 'vel_env'
    else:
        raise Exception('no env defined')

#   controller = PidController(conf.p_faktor, conf.i_faktor, conf.d_faktor,
#                              conf.iir_faktor, conf.iir_order, conf.max_output_controller)
    controller = AdaptivePidController(0, 0, 0, conf.iir_faktor, conf.iir_order,
                                       conf.max_output_controller)

    clock = pygame.time.Clock()
    episodes = 10
    for episode in range(episodes):
        observation = env.reset()
        error, measurement = observation

        done = False
        while not done:
            clock.tick(conf.fps)
            output = controller.give_output(error, measurement)

            observation, reward, done, info = env.step(output)
            error, measurement = observation

            env.render()


if __name__ == '__main__':
    main()
