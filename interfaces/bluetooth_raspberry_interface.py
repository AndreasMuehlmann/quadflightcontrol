from bluedot.btcomm import BluetoothServer

from interface_user import InterfaceUser


class BluetoothRaspberryInterface(InterfaceUser):
    def __init__(self):
        self.flight_control_status = True
        self.base_output = 0
        self.strength_x_slope = 0
        self.strength_y_slope = 0
        self.rotation = 0
        self.bluetooth_server = BluetoothServer(self.data_received)

    def give_inputs(self):
        return [self.base_output, self.strength_x_slope,
                self.strength_y_slope, self.rotation]

    def data_received(self, data):
        if data == "ON":
            self.flight_control_status = True

        if data == "OFF":
            self.flight_control_status = False

        split_data = data.split()

        if split_data[0]=="rotation:":
            self.rotation = float(split_data[1]) * 45

        elif split_data[0]=="height:":
            input_value = float(split_data[2]) * -1

            if input_value < 0:
                self.base_output = 100 + 300 * (input_value + 1)

            elif input_value >= 0:
                self.base_output = 400 + 300 * input_value

        elif split_data[0]=="direction:":
            self.strength_x_slope = float(split_data[1])
            self.strength_y_slope = float(split_data[2]) * -1

    def should_flight_control_run():
        return self.flight_control_status

    def send_message(self, message):
        pass

    def reset():
        pass
