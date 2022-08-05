from time import sleep

from hardware_interface import HardwareInterface


def main():
    hardware_interface = HardwareInterface()
    duration = 10
    iterations = 1000
    for i in range(iterations):
        hardware_interface.send_outputs([i for _ in range(4)])
        time.sleep(duration/iterations)

if __name__ == '__main__':
    main()
