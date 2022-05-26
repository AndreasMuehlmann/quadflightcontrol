import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
child = os.path.join(current_dir, 'pid_controller')
sys.path.append(child)
from pid_controller import PidController

from flight_control import FlightControl


class RobustFlightControl(FlightControl):
    def create_rotor_controller(self):
        return PidController(45, 20, 30, 0.9, 3, 1000)

    def give_output_rotor_controller(self, controller, target, measurement):
        return controller.give_output(target - measurement, measurement)
