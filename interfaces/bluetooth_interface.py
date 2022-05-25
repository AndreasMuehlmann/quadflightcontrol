from interface_user import InterfaceUser


class BluetoothInterface(InterfaceUser):
    def give_inputs(self):
        return [1, 1] #only for testing

    def send_outputs(self, outputs):
        pass
