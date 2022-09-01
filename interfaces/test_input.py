from time import sleep

from hardware_interface import HardwareInterface


def main():
    hardware_interface = HardwareInterface()

    try:
        while True:
            print(hardware_interface.give_measurements())
            sleep(0.05)

    except KeyboardInterrupt:
        hardware_interface.reset()
    hardware_interface.reset()
 

if __name__ == '__main__':
    main()
