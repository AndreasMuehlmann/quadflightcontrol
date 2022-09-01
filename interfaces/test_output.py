from time import sleep

from hardware_interface import HardwareInterface
from keyboard_interface import KeyboardInterface


def main():
    hardware_interface = HardwareInterface()
    keyboard_interface = KeyboardInterface()

    try:
        while True:
            base_output, strength_x_slope, strength_y_slope, rotation_vel = keyboard_interface.give_inputs()
            hardware_interface.send_outputs([100 * base_output for _ in range(4)])
            sleep(0.05)

    except KeyboardInterrupt:
        hardware_interface.reset()
    hardware_interface.reset()
 

if __name__ == '__main__':
    main()
