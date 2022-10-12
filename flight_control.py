import pygame
import time
import sys

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
        self.angle_controllers = [PidController(conf.angle_p_faktor, conf.angle_i_faktor,
                                                conf.angle_d_faktor, conf.iir_faktor,
                                                conf.iir_order, conf.max_output) \
                                                        for _ in range(4)]

        self.rotation_vel_controller = PidController(conf.rotation_vel_p_faktor, conf.rotation_vel_i_faktor,
                                                conf.rotation_vel_d_faktor, conf.iir_faktor,
                                                conf.iir_order, conf.max_output)

        self.interface_user = BluetoothRaspberryInterface()
        self.amount_inputs = 4

        self.interface_control = HardwareInterface()
        self.amount_rotor_angles = 4

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(conf.frequency)

            inputs = self.interface_user.give_inputs()
            if len(inputs) != self.amount_inputs:
                print('failure in collecting inputs')
                continue

            base_output, strength_x_slope_target, strength_y_slope_target, rotation_vel_target = inputs

            rotor_angles = self.interface_control.give_rotor_angles()
            if len(rotor_angles) != self.amount_rotor_angles:
                print('failure in collecting rotor angles or in measuring')
                continue

            rotor_angle_targets = give_rotor_angle_targets(strength_x_slope_target, strength_y_slope_target)
            rotation_vel = self.interface_control.give_rotation_vel()

            angle_controller_outputs = self._give_outputs_angle_controllers(rotor_angle_targets, rotor_angles)
            rotation_vel_controller_outputs = self._give_outputs_rotation_controller(rotation_vel_target, rotation_vel)

            outputs = [base_output +  angle_controller_output + rotation_vel_controller_output \
                    for angle_controller_output, rotation_vel_controller_output in zip(angle_controller_outputs, rotation_vel_controller_outputs)]
            outputs = self._remove_negatives(outputs)

            self.interface_control.send_outputs(outputs)

    def _give_outputs_angle_controllers(self, rotor_angle_targets, rotor_angles):
        return [self.angle_controllers[i].give_output(rotor_angle_targets[i] - rotor_angle, rotor_angle) \
                for i, rotor_angle in enumerate(rotor_angles)]

    def _give_outputs_rotation_controller(self, rotation_vel_target, rotation_vel):
        output = self.rotation_vel_controller.give_ouptut(target - rotation_vel, rotation_vel)
        return [output, -output, output, -output]


    def _remove_negatives(self, outputs):
        new_outputs = []
        for output in outputs: 
            if output < 0:
                output = 0
            new_outputs.append(output)
        
        return new_outputs

    def reset(self):
        self.interface_control.reset()
