import socket


class BluetoothClient():
    def __init__(self, bt_addr):
        self.bt_addr = bt_addr
        self.port = 0x1001
        self.size = 1024
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

        print(f'Trying to connect to {self.bt_addr} on PSM 0x{self.port}...')
        self.socket.connect((self.bt_addr, self.port))
        print('Connected.')

    def recv(self):
        return self.client_socket.recv(self.size)

    def send_message(self, message):
        self.socket.send(message)

    def reset(self):
        self.socket.close()
