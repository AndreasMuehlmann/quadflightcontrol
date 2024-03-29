import time

from csv_writer import Csv_Writer
from data_sender import DataSender


class DataLogger:
    def __init__(self):
        measurements_field_names = ['time', 'froll', 'fpitch', 'fyaw', 'altitude*100', 'faltitude*100']
        outputs_field_names = ['time', 'roll_c_o', 'pitch_c_o', 'yaw_c_o', 'altitude_c_o', 'ro1', 'ro2', 'ro3', 'ro4']
        self.measurements_csv_writer = Csv_Writer('measurements.csv', measurements_field_names)
        self.outputs_csv_writer = Csv_Writer('outputs.csv', outputs_field_names)
        self.data_sender = DataSender()
        for _ in range(50):
            self.data_sender.send_message('field_names:' + ','.join(measurements_field_names) \
                                          + ';' + ','.join(outputs_field_names))
            time.sleep(0.01)

    def log(self, measurements, outputs):
        measurements = [str(element) for element in measurements]
        outputs = [str(element) for element in outputs]
        self.measurements_csv_writer.add_line_of_data(measurements)
        self.outputs_csv_writer.add_line_of_data(outputs)
        self.data_sender.send_message(','.join(measurements) + ';' + ','.join(outputs))

    def turn_off(self):
        self.data_sender.turn_off()
        
