import sys
import os
import pygame
from copy import deepcopy
from abc import ABCMeta, abstractmethod

current_dir = os.path.dirname(os.path.abspath(__file__))
child = os.path.join(current_dir, 'interfaces')
sys.path.append(child)
from sim_interface import SimInterface
from bluetooth_interface import BluetoothInterface

from transform_input import give_heights


'''
(fl) rotor2 -> \ / <- rotor1 (fr)
                °
(bl) rotor3 -> / \ <- rotor4 (br)

[rotor1, rotor2, rotor2, rotor4]
'''


class FlightControl(metaclass=ABCMeta):
    def __init__(self):
        self.rotor_controllers = [self.create_rotor_controller() for _ in range(4)]

        self.interface_control = SimInterface()
        self.interface_user = BluetoothInterface()

        self.frequency = 100
        self.clock = pygame.time.Clock()

    @abstractmethod
    def create_rotor_controller():
        pass

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
            self.interface_control.send_outputs(outputs)

    def give_outputs(self, targets, measurements):
        outputs = []
        for i, measurement in enumerate(measurements):
            output = self.give_output_rotor_controller(self.rotor_controllers[i], targets[i], measurement)
            outputs.append(output)

        return outputs

    @abstractmethod
    def give_output_rotor_controller(self, controller, target, measurement):
        pass
