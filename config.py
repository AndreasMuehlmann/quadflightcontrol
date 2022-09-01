import os


# FLIGHT CONTROL
frequency = 100
max_angle_drone = 30


# CONTROLLER
controller = 'pid_controller'
max_output = 500


# TRAINING
load_checkpoint = True
learn = True

episodes_before_competing = 5
count_episodes_avg_over_for_competing = 10


# TESTING ENVIRONMENT
env = 'unity_sim_env' # The environments should be configured in quadflightcontrol/envs
total_time = 30 # per episode in s
delay = 0.05 # in s


# UNITYSIM
# PID_CONTROLLER
faktor = 0.5
p_faktor = 5
i_faktor = 0.05
d_faktor = 8
iir_faktor = 0.7 # for vel_env 0.85
iir_order = 3 # for vel_env 5

'''
# REALWORLD
# PID_CONTROLLER
p_faktor = 100
i_faktor = 1
d_faktor = 180
iir_faktor = 0.8 # for vel_env 0.85
iir_order = 3 # for vel_env 5
'''


# ADAPTIVE_PID_CONTROLLER
amount_prev_observations = 20


# AGENT
input_dims = (amount_prev_observations * 3 + 5,)
n_actions = 3
project_root = os.path.dirname(__file__)
chkpt_dir = os.path.join(project_root, 'adaptive_pid_controller', 'checkpoints', env)
layer_sizes = [256, 256, 128, 64, 32]
batch_size = 256
action_space_high = 1


# TRAINING
episodes = 100
range_avg = 10


# SIMULATION IN ENVS
window_width = 1600
window_height = 1000

default_x_stretch = 100
default_y_stretch = 12

x_dist_coord_sys = 1
y_dist_coord_sys = 10
