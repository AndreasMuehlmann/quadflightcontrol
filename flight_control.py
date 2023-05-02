import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import time

import pygame

import config as conf
from bluetooth_raspberry_interface import BluetoothRaspberryInterface
from data_sender import DataSender
from hardware_interface import HardwareInterface
from iir_filter import IirFilter
from csv_writer import Csv_Writer
from pid_flight_control import PidFlightControl


class FlightControl():
    def __init__(self):
        self.controller = PidFlightControl()

        self.interface_user = BluetoothRaspberryInterface()
        self.amount_inputs = 3

        self.interface_control = HardwareInterface()
        self.amount_rotor_angles = 4

        self.clock = pygame.time.Clock()
        self.time = 0

        self.angle_filters = [IirFilter(0.6, 1) for _ in range(4)]
        self.altitude_filter = IirFilter(0.9, 5)
        self.yaw_filter = IirFilter(0.6, 1)

        field_names = ['time', 'angle_rotor1', 'angle_rotor2', 'angle_rotor3', 'angle_rotor4',
                       'yaw', 'filtered_yaw', 'altitude', 'faltitude', 'output_rotor1', 'output_rotor2', 'output_rotor3', 'output_rotor4']
        self.csv_writer = Csv_Writer('data.csv', field_names)
        
        self.data_sender = DataSender()
        for _ in range(50):
            self.data_sender.send_message('field_names:' + ','.join(field_names))
            time.sleep(0.01)

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
            yaw = self.interface_control.give_yaw()
            altitude = self.interface_control.give_altitude()

            
            filtered_rotor_angles = self._give_filtered_list(rotor_angles,
                                                             self.angle_filters)
            filtered_altitude = self.altitude_filter.give_filtered(altitude)
            filtered_yaw = self.yaw_filter.give_filtered(yaw)

            outputs = self.controller.give_outputs(inputs, filtered_rotor_angles,
                                                   filtered_yaw, filtered_altitude)
            self.interface_control.send_outputs(outputs)
            data = [self.time] + filtered_rotor_angles + [yaw, filtered_yaw,
                 altitude * 200, filtered_altitude * 200] + [output/2 for output in outputs]
            data = [str(element) for element in data]
            self.csv_writer.add_line_of_data(data)
            self.data_sender.send_message(','.join(data))
            self.time += 1 / conf.frequency

    def _give_filtered_list(self, values, filters):
        filtered_values = []
        for value, filter in zip(values, filters):
            filtered_values.append(filter.give_filtered(value))
        return filtered_values

    def reset(self):
        self.altitude_filter.reset()
        self.yaw_filter.reset()
        self.controller.reset()
        self.interface_control.reset()

    def turn_off(self):
        self.data_sender.turn_off()
        self.interface_control.reset()
