import pygame
import math

import config as conf
from bluetooth_raspberry_interface import BluetoothRaspberryInterface
from hardware_interface import HardwareInterface
from fir_filter import FirFilter
from csv_writer import Csv_Writer


class FlightControl():
    def __init__(self):

        self.interface_user = BluetoothRaspberryInterface()
        self.amount_inputs = 4

        self.interface_control = HardwareInterface()
        self.amount_rotor_angles = 4

        self.clock = pygame.time.Clock()
        self.time = 0

        self.angle_filters = [FirFilter() for _ in range(4)]
        self.rotation_filter = FirFilter()
        self.height_vel_filter = FirFilter()

        self.csv_writer = Csv_Writer('data.csv', ['time', 'roll', 'yaw', ])

    def run(self):
        while True:
            self.clock.tick(conf.frequency)

            if not self.interface_user.should_flight_control_run():
                self.interface_control.send_outputs([0, 0, 0, 0])
                self.reset() 
                continue

            inputs = self.interface_user.give_inputs()
            if len(inputs) != self.amount_inputs:
                print('failure in collecting inputs')
                continue

            rotor_angles = self.interface_control.give_rotor_angles()
            if len(rotor_angles) != self.amount_rotor_angles:
                print('failure in collecting rotor angles or in measuring')
                continue
            rotation = self.interface_control.give_rotation()
            height_vel = self.interface_control.give_height_vel()

            filtered_rotor_angles = self._give_filtered_list(rotor_angles,
                                                             self.angle_filters)
            filtered_rotation = self.rotation_filter.give_filtered(rotation)
            filtered_height_vel = self.height_vel_filter.give_filtered(height_vel)

            outputs = self.controller.give_outputs(inputs, filtered_rotor_angles,
                                                   filtered_rotation, filtered_height_vel)
            self.interface_control.send_outputs(outputs)
            self.csv_writer.add_line_of_data([self.time] + rotor_angles +
                                             filtered_rotor_angles +
                                             [rotation, filtered_rotation,
                                              height_vel, filtered_height_vel])
            self.time += 1 / conf.frequency

    def _give_filtered_list(self, values, filters):
        filtered_values = []
        for value, filter in zip(values, filters):
            filtered_values.append(filter.give_filtered(value))
        return filtered_values

    def reset(self):
        self.controller.reset()
        for angle_filter in self.angle_filters:
            angle_filter.reset()
        self.rotation_filter.reset()
        self.height_vel_filter.reset()
