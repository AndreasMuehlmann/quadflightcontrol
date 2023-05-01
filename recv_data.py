import time
import traceback

import zmq

from csv_writer import Csv_Writer


def main():
    csv_writer = None
    context = zmq.Context()

    print('Connecting Raspberry Pi…')
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.178.122:5555")
    socket.setsockopt(zmq.SUBSCRIBE, b'flight_data:')
    print('Connected')
    try:
        while True:
            message = socket.recv().decode()
            message = message[message.find(':') + 1:]
            if message.startswith('field_names:'):
                csv_writer = Csv_Writer('data.csv', message[message.find(':') + 1:].split(','))
            elif csv_writer is not None:
                csv_writer.add_line_of_data(message.split(','))
            time.sleep(0.01)
    except Exception:
        context.destroy()
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
