from copy import deepcopy

import pygame

import config as conf
from sim_interface import SimInterface
from bluetooth_app_interface import BluetoothAppInterface
from keyboard_interface import KeyboardInterface
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
        self.rotor_controllers = [PidController(conf.p_faktor, conf.i_faktor,
                                                conf.d_faktor, conf.iir_faktor,
                                                conf.iir_order, conf.max_output_controller) \
                                  for _ in range(4)]

        self.interface_control = SimInterface()
        self.interface_user = KeyboardInterface()

        self.frequency = 100
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(self.frequency)

            inputs = self.interface_user.give_inputs()
            base_output = inputs[0]
            strength_x_slope = inputs[1]
            strength_y_slope = inputs[2]
            rotation_vel = inputs[3]

            angle_measurements = self.interface_control.give_measurements()
            if len(angle_measurements) != 4:
                print('failure in collecting measurements or in measuring')
                continue

            rotor_targets = give_heights(strength_x_slope, strength_y_slope)
            outputs = self.give_outputs_rotor_controllers(rotor_targets, angle_measurements)
            outputs = [output + base_output for output in outputs]

            self.interface_control.send_outputs(outputs)

    def give_outputs_rotor_controllers(self, targets, angle_measurements):
        outputs = []
        for i, angle_measurement in enumerate(angle_measurements):
            output = self.rotor_controllers[i].give_output(targets[i] - angle_measurement, angle_measurement)
            outputs.append(output)

        return outputs
