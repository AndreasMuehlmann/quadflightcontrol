import os

# The environments should be configured in quadflightcontrol/envs
from pos_env import PosEnv
from vel_env import VelEnv


env = 'vel_env'

window_width = 1200
window_height = 800

total_time = 30 #in s
delay = 0.05
delta_time = 0.05
fps = 5 / delta_time # 1 / delta_time is normal speed

max_output_controller = 1000

amount_prev_observations = 20


# PID_CONTROLLER
p_faktor = 400
i_faktor = 150
d_faktor = 300
iir_faktor = 0.8
iir_order = 3


# AGENT
input_dims = (amount_prev_observations * 3 + 5,)
n_actions = 3

project_root = os.path.dirname(__file__)
chkpt_dir = os.path.join(project_root, 'adaptive_pid_controller', 'checkpoints', env)
layer_sizes = [256, 256, 128, 64, 32]
batch_size = 256
action_space_high = 1

load_checkpoint = False
save_model = False
learn = False


# pos_env_iir_faktor = 0.8
# pos_env_iir_order = 3
# vel_env_iir_faktor = 0.85
# vel_env_iir_order = 5
