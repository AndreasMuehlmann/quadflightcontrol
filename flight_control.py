import pygame
import time

import config as conf
from sim_interface import SimInterface
from bluetooth_raspberry_interface import BluetoothRaspberryInterface
from bluetooth_server_interface import BluetoothServerInterface
from keyboard_interface import KeyboardInterface
from hardware_interface import HardwareInterface
from pid_controller import PidController
from give_rotor_angle_targets import give_rotor_angle_targets


class FlightControl():
    def __init__(self):
        self.rotor_controllers = [PidController(conf.p_faktor, conf.i_faktor,
                                                conf.d_faktor, conf.iir_faktor,
                                                conf.iir_order, conf.max_output) \
                                  for _ in range(4)]

        self.interface_user = BluetoothRaspberryInterface()
        self.amount_inputs = 4

        self.interface_control = HardwareInterface()
        self.amount_measurements = 4

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(conf.frequency)

            inputs = self.interface_user.give_inputs()
            if len(inputs) != self.amount_inputs:
                print('failure in collecting inputs')
                continue

            base_output, strength_x_slope, strength_y_slope, rotation_vel = inputs

            measurements = self.interface_control.give_measurements()
            # print(f'{round(measurements[0], 2)}, {round(measurements[1], 2)}, {round(measurements[2], 2)}, {round(measurements[3], 2)}')
            if len(measurements) != self.amount_measurements:
                print('failure in collecting measurements or in measuring')
                continue

            targets = give_rotor_angle_targets(strength_x_slope, strength_y_slope)

            outputs = self._give_outputs_rotor_controllers(targets, measurements)
            outputs = [output + base_output for output in outputs]
            outputs = self._remove_negatives(outputs)

            self.interface_control.send_outputs(outputs)

    def _give_outputs_rotor_controllers(self, targets, measurements):
        return [self.rotor_controllers[i].give_output(targets[i] - measurement, measurement) \
                for i, measurement in enumerate(measurements)]

    def _remove_negatives(self, outputs):
        new_outputs = []
        for output in outputs: 
            if output < 0:
                output = 0
            new_outputs.append(output)
        
        return new_outputs

