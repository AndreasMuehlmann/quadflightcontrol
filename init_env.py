import config as conf
from vel_env import VelEnv
from pos_env import PosEnv
from unity_sim_env import UnitySimEnv


def init_env():
    if conf.env == 'pos_env':
        return PosEnv()
    if conf.env == 'vel_env':
        return VelEnv()
    if conf.env == 'unity_sim_env':
        return UnitySimEnv()
    else:
        raise Exception(f'no env with name {conf.env} defined.')
