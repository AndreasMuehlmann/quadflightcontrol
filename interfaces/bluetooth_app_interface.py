from interface_user import InterfaceUser


class BluetoothAppInterface(InterfaceUser):
    def give_inputs(self):
        return [200, 0, 0, 0]

    def send_outputs(self, outputs):
        pass
