from interface_user import InterfaceUser


class BluetoothAppInterface(InterfaceUser):
    def give_inputs(self):
        return [1, 1] #only for testing

    def send_outputs(self, outputs):
        pass
