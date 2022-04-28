import random
import pygame

from  graph_repr import GraphRepr
from  pid_controller import PidController

SPEED_OF_SIMULATION = 100
INACCURACY = 0.05 #in m, of measurement


def random_num_p_or_n(upper_limit):
    if random.randint(0, 1) == 1:
        return random.random() * upper_limit
    return -random.random() * upper_limit

def main():
    delta_time = 0.01

    pos = 0
    vel = 0
    acc = 0

    last_acc = 0
    last_vel = 0

    target = 1

    error = target - pos
    pid_controller = PidController(6000)

    randomize_time = 0

    clock = pygame.time.Clock()
    graph = GraphRepr(1600, 1000)
    while True:
        clock.tick(SPEED_OF_SIMULATION)

        if randomize_time > 0.1:
            randomize_time = 0
            target += random_num_p_or_n(0.2)

        measured_pos = pos + random_num_p_or_n(INACCURACY) 
        rpm = pid_controller.give_output(target - measured_pos, measured_pos) 

        # calculation not accurate
        acc = rpm * 0.1

        vel += (acc + last_acc) / 2 * delta_time
        pos += (vel + last_vel) / 2 * delta_time
        

        graph.add_point(pid_controller.iir_measurement.outputs[-1])
        graph.target = target
        graph.re_draw()

        last_acc = acc
        last_vel = vel

        randomize_time += delta_time

if __name__ == '__main__':
    main()