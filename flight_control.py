import sys
import os
import pygame
from copy import deepcopy

current_dir = os.path.dirname(os.path.abspath(__file__))

child = os.path.join(current_dir, 'interfaces')
sys.path.append(child)
from sim_interface import SimInterface
from bluetooth_interface import BluetoothInterface

child = os.path.join(current_dir, 'pid_controller')
sys.path.append(child)
from pid_controller import PidController

from transform_input import give_heights


'''
(fl) rotor2 -> \ / <- rotor1 (fr)
                °
(bl) rotor3 -> / \ <- rotor4 (br)

[rotor1, rotor2, rotor2, rotor4]
'''


class FlightControl():
    def __init__(self):
        self.rotor_controllers = [PidController(4.5, 2.0, 3.0, 0.9, 3, 1000) for _ in range(4)]

        self.interface_control = SimInterface()
        self.interface_user = BluetoothInterface()

        self.frequency = 100
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

            inputs = self.interface_user.give_inputs()
            rotor_targets = give_heights(inputs[0], inputs[1])

            outputs = self.give_outputs(rotor_targets, measurements)
            print(outputs)
            self.interface_control.send_outputs(outputs)

    def give_outputs(self, targets, measurements):
        outputs = []
        for i, measurement in enumerate(measurements):
            output = self.rotor_controllers[i].give_output(targets[i] - measurement, measurement)
            outputs.append(output)

        return outputs
