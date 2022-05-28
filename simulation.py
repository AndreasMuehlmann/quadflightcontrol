import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
child = os.path.join(current_dir, 'envs')
sys.path.append(child)
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

    faktor = 10
    episodes = 10 
    for episode in range(episodes):
        observation = env.reset()
        done = False
        while not done:
            observation_, reward, done, info = env.step([0, 0, 0])
            env.pid_controller.p_faktor, env.pid_controller.i_faktor, env.pid_controller.d_faktor  = 40 * faktor, 15 * faktor, 30 * faktor
            env.render()
