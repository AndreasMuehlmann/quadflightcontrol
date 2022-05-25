import time
import os
import sys

from interface_control import InterfaceControl


class SimInterface(InterfaceControl):
    def __init__(self):
        with open('sim_interface_dir_path.txt', 'r') as file:
            self.path_to_interface = file.read().strip()
        self.path_interface = os.path.join(self.path_to_interface, 'interface_sim-control')
        print(self.path_interface)

        self.measurements_file = 'measurements.txt'
        self.outputs_file = 'outputs.txt'
        
        self.measurements_path = os.path.join(self.path_interface, self.measurements_file)
        self.outputs_path = os.path.join(self.path_interface, self.outputs_file)

        self.create_interface()

    def create_interface(self):
        try:
            os.mkdir(self.path_interface)
            print('created directory for interface.')
        except OSError:
            print('interface directory already exists.')

        self.create_file(self.measurements_path)
        self.create_file(self.outputs_path)

    def create_file(self, path):
        with open(path, 'w') as file:
            pass

    def give_measurements(self):
        try:
            with open(self.measurements_path, 'r') as file:
                lines = file.readlines()
        except IOError:
            time.sleep(1/1000)
            return read_measurements()

        measurements = []
        for line in lines: 
            measurements.append(float(line))

        return [0.1, 0.1, -0.1, -0.1]
        return measurements

    def send_outputs(self,outputs):
        with open(self.outputs_path, 'w') as file:
            try:
                for output in outputs:
                     file.write(f'{output}\n')
            except IOExeption:
                time.sleep(1/1000)
                write_outputs(outputs_path, outputs)

