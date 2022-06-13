from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from vel_env import VelEnv
from pos_env import PosEnv


if __name__ == '__main__':
    env = PosEnv()

    if type(env) == PosEnv:
        env_kind = 'pos_env'
    elif type(env) == VelEnv:
        env_kind = 'vel_env'
    else:
        raise Exception('no env defined')

    episodes = 10
    for episode in range(episodes):
        observation = env.reset()
        done = False
        while not done:
            observation_, reward, done, info = env.step([0, 0, 0])
            env.render()
