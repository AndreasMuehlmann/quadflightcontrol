delay = 0.05
window_width = 1200
window_height = 800

total_time = 30 #in s
time_available = total_time

delta_time = 0.05

fps = 1  / delta_time # move this to where it is needed

last_small_target_change = total_time
last_big_target_change = total_time
last_env_force_change = total_time

amount_prev_errors = int(2 / delta_time)

# AGENT
input_dims = 0
n_actions = 0
chkpt_dir = 0
layer_sizes = 0
batch_size = 0

# PID_CONTROLLER
p_faktor = 400
i_faktor = 150
d_faktor = 300
max_output_controller = 1000

# POS_ENV
pos_env_inaccuracy = 0.05
pos_env_iir_faktor = 0.8
pos_env_iir_order = 3

pos_env_range_positive_reward = 0.05
pos_env_bad_error = 0.2
pos_env_bad_produced_acc = 5

pos_env_time_without_small_target_change = 0.2
pos_env_time_without_big_target_change = 4
pos_env_time_without_env_force_change = 3

pos_env_max_faktor = 0.1
pos_env_min_faktor = 0.02

pos_env_max_env_force = 10 # strength is same as output
pos_env_min_env_force = -pos_env_max_env_force

pos_env_max_target =  0.5 # 1
pos_env_min_target = -pos_env_max_target

pos_env_max_output = 1000
pos_env_min_output = -pos_env_max_output

pos_env_max_small_target_change = 0.1
pos_env_max_big_target_change = abs(pos_env_max_target) + abs(pos_env_min_target)
pos_env_max_env_force_change = abs(pos_env_max_env_force) + abs(pos_env_min_env_force)

pos_env_max_positive_reward = pos_env_bad_error * 10


# VEL_ENV
vel_env_inaccuracy = 0.2
vel_env_iir_faktor = 0.85
vel_env_iir_order = 5

vel_env_range_positive_reward = 0.5
vel_env_bad_error = 3
vel_env_bad_produced_acc = 10

vel_env_time_without_small_target_change = 0.2
vel_env_time_without_big_target_change = 4
vel_env_time_without_env_force_change = 3

vel_env_max_faktor = 0.1
vel_env_min_faktor = 0.04

vel_env_max_env_force = 15
vel_env_min_env_force = vel_env_max_env_force

vel_env_max_target = 10
vel_env_min_target = vel_env_max_target

vel_env_max_output = 1000
vel_env_min_output = vel_env_max_output

vel_env_max_small_target_change = 0.6
vel_env_max_big_target_change = abs(vel_env_max_target) + abs(vel_env_min_target)
vel_env_max_env_force_change = abs(vel_env_max_env_force) + abs(vel_env_min_env_force)

vel_env_max_positive_reward = pos_env_bad_error * 10
