import bluetooth

from interface_user import InterfaceUser


class BluetoothServerInterface(InterfaceUser):
    def __init__(self):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.port = 0x1001
        self.backlog = 1
        self.size = 1024

        self.server_socket.bind(("", self.port))
        self.server_socket.listen(self.backlog)
        self.client_socket, address = self.server_socket.accept()
        print("Accepted connection from", address)
        data = self.client_socket.recv(self.size)

    def give_inputs(self):
        data = self.client_socket.recv(self.size)

        string_inputs = data.decode('utf-8').split(',')
        inputs = [float(string_input) for string_input in string_inputs]

        return inputs

    def send_message(self, message):
        self.client_socket.send(message)

    def reset():
        self.client_socket.close()
        self.server_socket.close()
