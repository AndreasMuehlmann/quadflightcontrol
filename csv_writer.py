import csv


class Csv_Writer:
    def __init__(self, file_name, field_names):
        self.file_name = file_name
        self.field_names = field_names
        self._create_file_with_headers()

    def _create_file_with_headers(self):
        with open(self.file_name, 'w') as csv_file:
            dict_writer = csv.DictWriter(csv_file, self.field_names)
            dict_writer.writeheader()

    def add_line_of_data(self, data):
        with open(self.file_name, 'a') as csv_file:
            dict_writer = csv.DictWriter(csv_file, self.field_names)
            data_dict = {key_value_pair[0]: key_value_pair[1]
                         for key_value_pair in zip(self.field_names, data)}
            dict_writer.writerow(data_dict)
