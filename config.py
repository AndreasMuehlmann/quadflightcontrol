import os


# FLIGHT CONTROL
frequency = 100 
max_angle_drone = 10


# CONTROLLER
controller = 'pid_controller'
max_output = 500


# TRAINING
load_checkpoint = True
learn = True

episodes_before_competing = 5
count_episodes_avg_over_for_competing = 10


# TESTING ENVIRONMENT
env = 'real_world_env' # The environments should be configured in quadflightcontrol/envs
total_time = 30 # per episode in s
delay = 0.05 # in s


'''
# UNITYSIM
# PID_CONTROLLER
p_faktor = 5
i_faktor = 0.05
d_faktor = 8
iir_faktor = 0.7 # for vel_env 0.85
iir_order = 3 # for vel_env 5
'''

# REALWORLD
# ANGLE_PID_CONTROLLER
angle_p_faktor = 0.7 # 1.38 # 
angle_i_faktor = 0.65 # 1.25 # 
angle_d_faktor = 0.6 # 0.6

# ROTATION_PID_CONTROLLER
rotation_p_faktor = 0.5
rotation_i_faktor = 0.4
rotation_d_faktor = 0.8

iir_faktor = 0.7
iir_order = 3


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
