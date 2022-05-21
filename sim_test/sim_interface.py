import time
import os
import sys
from random import random
from copy import deepcopy
from transform_input import give_heights

current_dir = os.path.dirname(os.path.abspath(__file__))
child = os.path.join(current_dir, 'pid_controller')
sys.path.append(child)
from pid_controller import PidController


def create_interface(path_interface, measurements_path, outputs_path):
    try:
        os.mkdir(path_interface)
        print('created directory for interface.')
    except OSError:
        print('interface directory already exists.')

    create_file(os.path.join(path_interface, measurements_path))
    create_file(os.path.join(path_interface, outputs_path))


def create_file(path):
    with open(path, 'w') as file:
        pass


def read_measurements(measurements_path):
    try:
        with open(measurements_path, 'r') as file:
            lines = file.readlines()
    except IOError:
        time.sleep(1/1000)
        return read_measurements()

    measurements = []
    for line in lines: 
        measurements.append(float(line))

    return measurements


def write_outputs(outputs_path, outputs):
    with open(outputs_path, 'w') as file:
        try:
            for output in outputs:
                 file.write(f'{output}\n')
        except IOExeption:
            time.sleep(1/1000)
            write_outputs(outputs_path, outputs)


def main():
    assert len(sys.argv) == 2, 'The programm requires a  path to where the interface should be.'\
                               + 'This path has to be the same for this programm and the running simulation.'

    path_interface = os.path.join(sys.argv[1], 'interface_sim-control')

    measurements_file = 'measurements.txt'
    outputs_file = 'outputs.txt'
    
    measurements_path = os.path.join(path_interface, measurements_file)
    outputs_path = os.path.join(path_interface, outputs_file)

    create_interface(path_interface, measurements_path, outputs_path)

    controllers = [PidController(45, 20, 30, 0.8, 3, 1000) for i in range(4)]


    prev_measurements = None
    while True:
        time.sleep(1/20)

        measurements = read_measurements(measurements_path)

        if len(measurements) > 0:
            prev_measurements = deepcopy(measurements)
        else:
            if prev_measurements is None:
                continue
            measurements = deepcopy(prev_measurements)

        print(measurements)
        heights = give_heights(1, 1)

        outputs = []
        for i, measurement in enumerate(measurements):
            outputs.append(controllers[i].give_output(heights[i] - measurement, measurement))

        write_outputs(outputs_path, outputs)
        


if __name__ == '__main__':
    main()

