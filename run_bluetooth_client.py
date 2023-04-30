import sys
import socket

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from bluetooth_client import BluetoothClient
from csv_writer import Csv_Writer


def main():
    assert len(sys.argv) == 2, 'The Programm takes one argument ' \
        + f', the bluetooth address of the server ({len(sys.argv)} where given).'
    bt_addr = sys.argv[1]
    csv_writer = None
    bluetooth_client = BluetoothClient(bt_addr)
    try:
        while True:
            message = bluetooth_client.recv()
            if message.startwith('field_names:'):
                print(message[:message.find(':') + 1])
                csv_writer = Csv_Writer('bluetooth_data', message[:message.find(':')])
            if csv_writer is None:
                continue
            csv_writer.add_line_of_data(message.split(','))

    except KeyboardInterrupt:
        bluetooth_client.reset()


if __name__ == '__main__':
    main()
