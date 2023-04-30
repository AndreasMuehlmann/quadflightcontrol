import bluetooth

from keyboard_interface import KeyboardInterface


class BluetoothClient():
    def __init__(self, bt_addr):
        self.socket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.bt_addr = bt_addr
        self.port = 0x1001
        self.size = 1024

        print(f'Trying to connect to {self.bt_addr} on PSM 0x{self.port}...')
        self.socket.connect((self.bt_addr, self.port))
        print('Connected.')

    def recv(self):
        return self.client_socket.recv(self.size)

    def send(self, data):
        self.socket.send(data)

    def reset(self):
        self.socket.close()
