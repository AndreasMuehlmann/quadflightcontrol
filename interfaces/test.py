from time import sleep

import RPi.GPIO as gpio # this just works on a raspberry pi

from hardware_interface import HardwareInterface


def main():
    hardware_interface = HardwareInterface()
    duration = 10
    iterations = 1000
    for i in range(iterations):
        hardware_interface.send_outputs([i for _ in range(4)])
        sleep(duration/iterations)
        
    gpio.cleanup()
 

if __name__ == '__main__':
    main()
