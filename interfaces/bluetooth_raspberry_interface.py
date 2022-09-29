from bluedot.btcomm import BluetoothServer

from interface_user import InterfaceUser


class BluetoothRaspberryInterface(InterfaceUser):

    def __init__(self):
        self.base_output = 0
        self.strength_x_slope = 0
        self.strength_y_slope = 0
        self.rotation_vel = 0
        self.bluetooth_server = BluetoothServer(self.data_received)

    def give_inputs(self):
        return [self.base_output, self.strength_x_slope,
                self.strength_y_slope, self.rotation_vel]

    def data_received(self, data):
        split_data = data.split()

        if split_data[0]=="rotation:":
            self.rotation_vel = float(split_data[1])

        elif split_data[0]=="height:":
            self.base_output = float(split_data[2]) * -1

        elif split_data[0]=="direction:":
            self.strength_x_slope = float(split_data[1])
            self.strength_y_slope = float(split_data[2]) * -1

    def send_message(self, message):
        pass

    def reset():
        pass





