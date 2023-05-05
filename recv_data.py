import time
import traceback

import zmq

from csv_writer import Csv_Writer


def main():
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.178.122:5555")
    socket.setsockopt(zmq.SUBSCRIBE, b'flight_data:')
    try:
        while True:
            message = socket.recv().decode()
            message = message[message.find(':') + 1:]
            if message.startswith('field_names:'):
                message = message[message.find(':') + 1:]
                measurements_message = message[:message.find(';')]
                outputs_message = message[message.find(';') + 1:]
                measurements_csv_writer = Csv_Writer('measurements.csv', measurements_message.split(','))
                outputs_csv_writer = Csv_Writer('outputs.csv', outputs_message.split(','))
            else:
                measurements_message = message[:message.find(';')]
                outputs_message = message[message.find(';') + 1:]
                measurements_csv_writer.add_line_of_data(measurements_message.split(','))
                outputs_csv_writer.add_line_of_data(outputs_message.split(','))
            time.sleep(0.01)
    except Exception:
        context.destroy()
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
