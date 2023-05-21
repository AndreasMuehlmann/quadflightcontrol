import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

import config as conf
from bluetooth_raspberry_interface import BluetoothRaspberryInterface
from hardware_interface import HardwareInterface
from iir_filter import IirFilter
from pid_flight_control import PidFlightControl
from calibration_controller import CalibrationController
from data_logger import DataLogger


class FlightControl():
    def __init__(self):
        self.controller = CalibrationController()
        self.interface_user = BluetoothRaspberryInterface()
        self.interface_control = HardwareInterface()
        self.data_logger = DataLogger()

        self.clock = pygame.time.Clock()
        self.time = 0

        self.angle_filters = [IirFilter(0.6, 2) for _ in range(2)]
        self.yaw_filter = IirFilter(0.6, 1)
        self.altitude_filter = IirFilter(0.8, 1)
        self.rotor_output_filters = [IirFilter(0.6, 1) for _ in range(4)]

    def run(self):
        while True:
            self.clock.tick(conf.frequency)

            inputs = self.interface_user.give_inputs()
            if len(inputs) != 3:
                print('failure in collecting inputs')
                continue

            rotor_angles = self.interface_control.give_rotor_angles()
            yaw = self.interface_control.give_yaw()
            self.altitude = self.interface_control.give_altitude()

            self.filtered_rotor_angles = rotor_angles # self._give_filtered_list(rotor_angles,
                                                      #       self.angle_filters)
            self.filtered_altitude = self.altitude_filter.give_filtered(self.altitude)
            self.filtered_yaw = self.yaw_filter.give_filtered(yaw)

            self.rotor_outputs = self.controller.give_outputs(inputs, self.filtered_rotor_angles,
                                                         self.filtered_yaw, self.filtered_altitude)
            # self.rotor_outputs = self._give_filtered_list(self.rotor_outputs, self.rotor_output_filters)

            self.data_logger.log(self._give_to_log_measurements(), self._give_to_log_outputs())
            if not self.interface_user.should_flight_control_run():
                self.reset()
                continue

            if self._should_turn_off():
                self.turn_off()
                break

            self.interface_control.send_outputs(self.rotor_outputs)
            self.time += 1 / conf.frequency

    def _give_to_log_measurements(self):
        return [self.time] + self.filtered_rotor_angles[:2] + \
               [self.filtered_yaw, self.altitude * 100, self.filtered_altitude * 100]

    def _give_to_log_outputs(self):
        return [self.time] + self.controller.rotor_outputs_angle_controllers[:2] \
            + [self.controller.yaw_controller_output, self.controller.altitude_controller_output] \
            + self.rotor_outputs

    def _should_turn_off(self):
        return abs(self.filtered_altitude) > 2 or abs(self.filtered_yaw) > 140 \
                or abs(self.filtered_rotor_angles[0]) > 20 or abs(self.filtered_rotor_angles[1]) > 20

    def _give_filtered_list(self, values, filters):
        filtered_values = []
        for value, digital_filter in zip(values, filters):
            filtered_values.append(digital_filter.give_filtered(value))
        return filtered_values

    def reset(self):
        self.interface_control.reset()

    def turn_off(self):
        self.data_logger.turn_off()
        self.interface_control.reset()
