import config as conf
from unity_sim_roll_env import UnitySimRollEnv
from real_world_altitude_env import RealWorldAltitudeEnv


def init_env():
    if conf.env == 'unity_sim_env':
        return UnitySimRollEnv()
    if conf.env == 'real_world_altitude_env':
        return RealWorldAltitudeEnv()
    else:
        raise Exception(f'no env with name {conf.env} defined.')
