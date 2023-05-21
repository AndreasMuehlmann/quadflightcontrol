import os


# FLIGHT CONTROL
frequency = 100 
max_angle_drone = 5
max_output = 1000


# CONTROLLER
controller = 'pid_controller'


# TRAINING
load_checkpoint = True
learn = True

episodes_before_competing = 5
count_episodes_avg_over_for_competing = 10


# TESTING ENVIRONMENT
env = 'real_world_altitude_env' # The environments should be configured in quadflightcontrol/envs
total_time = 30 # per episode in s
delay = 0.2 # in s


'''
# UNITYSIM
# PID_CONTROLLER
p_faktor = 5
i_faktor = 0.05
d_faktor = 8
iir_faktor = 0.7 # for vel_env 0.85
iir_order = 3 # for vel_env 5
'''

# PID-CONTROLLER FOR GRAPH-SIMULATION
p_faktor = 58.6 # 150 # 84.375 # 37.5
i_faktor = 12.2 # 50 # 21.09 # 6.25
d_faktor = 93.75 # 150 # 112.5 # 75

# REALWORLD
# ANGLE_PID_CONTROLLER
angle_p_faktor = 3.2
angle_i_faktor = 0
angle_d_faktor = 0.14333

# YAW_PID_CONTROLLER
yaw_p_faktor = 0
yaw_i_faktor = 0
yaw_d_faktor = 0


# HEIHT_VEL_PID_CONTROLLER
altitude_p_faktor = 20
altitude_i_faktor = 10
altitude_d_faktor = 0


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
