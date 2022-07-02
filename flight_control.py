import pygame

import config as conf
from sim_interface import SimInterface
from bluetooth_app_interface import BluetoothAppInterface
from keyboard_interface import KeyboardInterface
from pid_controller import PidController
from transform_input import give_heights


class FlightControl():
    def __init__(self):
        self.rotor_controllers = [PidController(conf.p_faktor, conf.i_faktor,
                                                conf.d_faktor, conf.iir_faktor,
                                                conf.iir_order, conf.max_output_controller) \
                                  for _ in range(4)]

        self.interface_user = KeyboardInterface()
        self.amount_inputs = 4

        self.interface_control = SimInterface()
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
            if len(measurements) != self.amount_measurements:
                print('failure in collecting measurements or in measuring')
                continue

            targets = give_rotor_angle_targets(strength_x_slope, strength_y_slope)

            outputs = self._give_outputs_rotor_controllers(targets, measurements)
            outputs = [output + base_output for output in outputs]

            self.interface_control.send_outputs(outputs)

    def _give_outputs_rotor_controllers(self, targets, measurements):
        return [self.rotor_controllers[i].give_output(targets[i] - measurement, measurement) \
                for i, measurement in enumerate(measurements)]
