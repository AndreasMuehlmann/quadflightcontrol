from pos_env import PosEnv


# TODO: make default values in PosEnv
# TODO: everything with init (no init_values) call super init in the end for default values
# TODO: should_reset into controller env
# TODO: adjust values to UnitySim
# TODO: make pid_controller faktor adjust to environment (inherit from pid_controller)
# TODO: maybe remove self.faktor from self.env_force


class UnitySimEnv(PosEnv):
    def __init__(self):
        super(UnitySimEnv, self).__init__()

    def _init_values(self):
        self.inaccuracy = 0.05

        self.range_positive_reward = 0.05
        self.bad_error = 0.2
        self.max_positive_reward = self.bad_error * 10
        self.bad_produced_acc = 5

        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_force_change = 3

        self.max_faktor = 1 / 4
        self.min_faktor = self.max_faktor

        self.max_env_force = -1
        self.min_env_force = self.max_env_force

        self.max_target =  0.3 # 1
        self.min_target = -self.max_target

        self.max_output = 1000
        self.min_output = -self.max_output

        self.max_small_target_change = 0.05
        self.max_big_target_change = abs(self.max_target) + abs(self.min_target)
        self.max_env_force_change = abs(self.max_env_force) + abs(self.min_env_force)
