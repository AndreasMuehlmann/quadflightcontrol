from pos_env import PosEnv


class UnitySimEnv(PosEnv):
    def __init__(self):
        super(UnitySimEnv, self).__init__()

    def _init_values(self):
        self.inaccuracy = 0.2

        # this is not up to date
        self.range_positive_reward = 0.05
        self.bad_error = 0.2
        self.max_positive_reward = self.bad_error * 10
        self.bad_produced_acc = 5

        self.time_without_small_target_change = 0.2
        self.time_without_big_target_change = 4
        self.time_without_env_output_change = 3

        self.max_faktor = 1
        self.min_faktor = self.max_faktor

        self.max_env_output = -0
        self.min_env_output = self.max_env_output

        self.max_target = 30
        self.min_target = -self.max_target

        self.max_small_target_change = 3
        self.max_big_target_change = abs(self.max_target) + abs(self.min_target)
        self.max_env_output_change = abs(self.max_env_output) + abs(self.min_env_output)
