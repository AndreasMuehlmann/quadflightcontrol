import sys
import os
import pygame
from copy import deepcopy

current_dir = os.path.dirname(os.path.abspath(__file__))

child = os.path.join(current_dir, 'pid_controller')
sys.path.append(child)
from pid_controller import PidController

child = os.path.join(current_dir, 'interfaces')
sys.path.append(child)
from sim_interface import SimInterface
from interface_control import InterfaceControl

from flight_control import FlightControl
from transform_input import give_heights


#TODO: use interface_user for inputs


class RobustFlightControl(FlightControl):
    def __init__(self):
        self.frequency = 100
        self.rotor_controllers = [PidController(45, 20, 30, 0.8, 3, 1000) for i in range(4)]

        self.interface_control = SimInterface()
        self.interface_user = None

        self.clock = pygame.time.Clock()

    def run(self):
        prev_measurements = None
        while True:
            self.clock.tick(self.frequency)
            
            measurements = self.interface_control.give_measurements()

            if len(measurements) == 4:
                prev_measurements = deepcopy(measurements)
            else:
                print('failure in collecting measurements or in measuring')
                if prev_measurements is None:
                    continue
                measurements = deepcopy(prev_measurements)

            outputs = self.give_outputs(measurements)
            self.interface_control.send_outputs(outputs)

    def give_outputs(self, measurements):
        rotor_targets = give_heights(1, 1)

        outputs = []
        for i, measurement in enumerate(measurements):
            outputs.append(self.rotor_controllers[i].give_output(rotor_targets[i] - measurement, measurement))

        return outputs

