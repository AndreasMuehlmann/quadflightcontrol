from bluedot.btcomm import BluetoothServer

from give_rotor_angle_targets import give_rotor_angle_targets


class BluetoothRaspberryInterface():
    def __init__(self):
        self.flight_control_status = True
        self.altitude_difference = 0
        self.strength_x_slope = 0
        self.strength_y_slope = 0
        self.yaw_difference = 0
        self.bluetooth_server = BluetoothServer(self.data_received)

    def give_inputs(self):
        rotor_angle_targets = give_rotor_angle_targets(self.strength_x_slope,
                                                       self.strength_y_slope)
        return [self.altitude_difference, rotor_angle_targets, self.yaw_difference]

    def data_received(self, data):
        if data.strip() == 'ON':
            self.flight_control_status = True

        if data.strip() == 'OFF':
            self.flight_control_status = False

        split_data = data.split()

        if split_data[0]=="rotation:":
            self.yaw_difference = float(split_data[1]) * 0.1

        elif split_data[0]=="height:":
            self.altitude_difference = float(split_data[2]) * -0.1

        elif split_data[0]=="direction:":
            self.strength_x_slope = float(split_data[1])
            self.strength_y_slope = float(split_data[2]) * -1

    def should_flight_control_run(self):
        return self.flight_control_status
