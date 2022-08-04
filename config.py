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
env = 'real_world_env' # The environments should be configured in quadflightcontrol/envs
total_time = 30 # per episode in s
delay = 0.05 # in s


# PID_CONTROLLER
p_faktor = 15
i_faktor = 3
d_faktor = 18
iir_faktor = 0.8 # for vel_env 0.85
iir_order = 3 # for vel_env 5


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



# SIMULATION IN ENVS
episodes = 100
range_avg = 10
window_width = 1200
window_height = 800

default_x_stretch = 100
default_y_stretch = 50
