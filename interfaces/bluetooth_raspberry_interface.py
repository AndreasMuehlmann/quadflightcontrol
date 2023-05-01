from bluedot.btcomm import BluetoothServer

from give_rotor_angle_targets import give_rotor_angle_targets


class BluetoothRaspberryInterface():
    def __init__(self):
        self.flight_control_status = True
        self.height_vel = 0
        self.strength_x_slope = 0
        self.strength_y_slope = 0
        self.rotation = 0
        self.bluetooth_server = BluetoothServer(self.data_received)

    def give_inputs(self):
        rotor_angle_targets = give_rotor_angle_targets(self.strength_x_slope,
                                                       self.strength_y_slope)
        return [self.height_vel, rotor_angle_targets, self.rotation]

    def data_received(self, data):
        if data == "ON":
            self.flight_control_status = True

        if data == "OFF":
            self.flight_control_status = False

        split_data = data.split()

        if split_data[0]=="rotation:":
            self.rotation = float(split_data[1]) * 0.1

        elif split_data[0]=="height:":
            self.height_vel = float(split_data[2]) * -1

        elif split_data[0]=="direction:":
            self.strength_x_slope = float(split_data[1])
            self.strength_y_slope = float(split_data[2]) * -1

    def should_flight_control_run(self):
        return self.flight_control_status

    def send_message(self, message):
        pass

    def reset():
        pass
