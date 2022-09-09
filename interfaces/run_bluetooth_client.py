import sys

from keyboard_interface import KeyboardInterface
from bluetooth_client import BluetoothClient


def main():
    assert len(sys.argv) == 2, 'The Programm takes one argument ' \
        + f', the bluetooth address of the server ({len(sys.argv)} where given).'
    bt_addr = sys.argv[1]

    bluetooth_client = BluetoothClient(bt_addr)
    keyboard_interface = KeyboardInterface()

    try:
        while True:
            inputs = keyboard_interface.give_inputs()
            bluetooth_client.send_data(f'{round(inputs[0])},{inputs[1]},{inputs[2]},{inputs[3]}')
    except KeyboardInterrupt:
        bluetooth_client.reset()


if __name__ == '__main__':
    main()
