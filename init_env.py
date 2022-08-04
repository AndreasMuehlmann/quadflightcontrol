import config as conf
from vel_env import VelEnv
from pos_env import PosEnv
from unity_sim_env import UnitySimEnv
from real_world_env import RealWorldEnv


def init_env():
    if conf.env == 'pos_env':
        return PosEnv()
    if conf.env == 'vel_env':
        return VelEnv()
    if conf.env == 'unity_sim_env':
        return UnitySimEnv()
    if conf.env == 'real_world_env':
        return RealWorldEnv()
    else:
        raise Exception(f'no env with name {conf.env} defined.')
