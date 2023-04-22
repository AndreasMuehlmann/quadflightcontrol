import pygame

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from pid_controller import PidController
from iir_filter import IirFilter
from fir_filter import FirFilter
import config as conf
from init_env import init_env
from csv_writer import Csv_Writer


def run_episode(env, controller, learn=False):
    clock = pygame.time.Clock()
    time = 0

    observation = env.reset()
    error, measurement = observation

    controller.reset()

    score = 0
    done = False

    csv_writer = Csv_Writer('data.csv', ['time', 'measurement', 'filtered_measurement'])
    error_filter = FirFilter()
    measurement_filter = FirFilter()
    while not done:
        clock.tick(conf.frequency)

        filtered_error = error_filter.give_filtered(error)
        filtered_measurement = measurement_filter.give_filtered(measurement)
        output = controller.give_output(filtered_error, filtered_measurement)
        csv_writer.add_line_of_data([time, measurement, filtered_measurement])

        observation, reward, done, info = env.step(output)
        error, measurement = observation
        score += reward
        env.render()
        time += 1/conf.frequency

    return score


if __name__ == '__main__':
    controller = PidController(conf.angle_p_faktor, conf.angle_i_faktor, conf.angle_d_faktor, conf.max_output)
    score = run_episode(init_env(), controller)
    print(score)
