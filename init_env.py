import config as conf
from vel_env import VelEnv
from pos_env import PosEnv


def init_env():
    if conf.env == 'pos_env':
        return PosEnv()
    if conf.env == 'vel_env':
        return VelEnv()
    else:
        raise Exception(f'no env with name {conf.env} defined.')
