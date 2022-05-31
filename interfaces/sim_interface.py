import os

from interface_control import InterfaceControl


class SimInterface(InterfaceControl):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_file_with_interface_dir = os.path.join(current_dir, 'sim_interface_dir_path.txt')
        with open(path_to_file_with_interface_dir, 'r') as file:
            self.path_to_interface = file.read().strip()
        self.path_interface = os.path.join(self.path_to_interface, 'interface_sim-control')

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
            return self.read_measurements()

        measurements = []
        for line in lines: 
            line = line.replace(',', '.').strip()
            measurements.append(float(line))

        return measurements

    def send_outputs(self,outputs):
        try:
            with open(self.outputs_path, 'w') as file:
                for output in outputs:
                    output_string = str(output).replace('.', ',')
                    file.write(f'{output_string}\n')
        except IOError:
            self.send_outputs(outputs)

