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
        self.interface_control = HardwareInterface()

        self.clock = pygame.time.Clock()
        self.time = 0

        self.angle_filters = [IirFilter(0.6, 1) for _ in range(4)]
        self.yaw_filter = IirFilter(0.6, 1)
        self.altitude_filter = IirFilter(0.9, 5)

        measurements_field_names = ['time', 'fangle_rotor1', 'fangle_rotor2', 'fangle_rotor3', 'fangle_rotor4',
                       'yaw', 'fyaw', 'altitude', 'faltitude']
        outputs_field_names = ['angle_controller_output1', 'angle_controller_output2', 'angle_controller_output3',
                              'angle_controller_output4', 'yaw_controller_output', 'altitude_controller_output',
                              'rotor_output1', 'rotor_output2', 'rotor_output3', 'rotor_output4']
        self.measurements_csv_writer = Csv_Writer('measurements.csv', measurements_field_names)
        self.outputs_csv_writer = Csv_Writer('outputs.csv', outputs_field_names)
        self.data_sender = DataSender()
        for _ in range(50):
            self.data_sender.send_message('field_names:' + ','.join(measurements_field_names) \
                                          + ';' + ','.join(outputs_field_names))
            time.sleep(0.01)

    def run(self):
        while True:
            self.clock.tick(conf.frequency)

            inputs = self.interface_user.give_inputs()
            if len(inputs) != 3:
                print('failure in collecting inputs')
                continue

            rotor_angles = self.interface_control.give_rotor_angles()
            yaw = self.interface_control.give_yaw()
            altitude = self.interface_control.give_altitude()

            filtered_rotor_angles = self._give_filtered_list(rotor_angles,
                                                             self.angle_filters)
            filtered_altitude = self.altitude_filter.give_filtered(altitude)
            filtered_yaw = self.yaw_filter.give_filtered(yaw)

            rotor_outputs = self.controller.give_outputs(inputs, filtered_rotor_angles,
                                                   filtered_yaw, filtered_altitude)
            measurements = [self.time] + filtered_rotor_angles + \
                [yaw, filtered_yaw, altitude * 200, filtered_altitude * 200]
            outputs = [rotor_output / 2 for rotor_output in rotor_outputs] + self.controller.rotor_outputs_angle_controllers \
                + [self.controller.yaw_controller_output, self.controller.altitude_controller_output]
            measurements = [str(element) for element in measurements]
            outputs = [str(element) for element in outputs]
            self.measurements_csv_writer.add_line_of_data(measurements)
            self.outputs_csv_writer.add_line_of_data(outputs)
            self.data_sender.send_message(','.join(measurements) + ';' + ','.join(outputs))

            if not self.interface_user.should_flight_control_run():
                self.reset() 
                continue

            self.interface_control.send_outputs(rotor_outputs)
            self.time += 1 / conf.frequency

    def _give_filtered_list(self, values, filters):
        filtered_values = []
        for value, digital_filter in zip(values, filters):
            filtered_values.append(digital_filter.give_filtered(value))
        return filtered_values

    def reset(self):
        self.altitude_filter.reset()
        self.yaw_filter.reset()
        self.controller.reset()
        self.interface_control.reset()

    def turn_off(self):
        self.data_sender.turn_off()
        self.interface_control.reset()
