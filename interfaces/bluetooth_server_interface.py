import socket


class BluetoothServerInterface():
    def __init__(self):
        self.bt_addr = 'E4:5F:01:B1:77:A1'
        self.port = 3
        self.backlog = 1
        self.size = 1024
        self.server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.server_socket.bind((self.bt_addr, self.port))
        self.server_socket.listen(self.backlog)

        self.server_socket.bind(("", self.port))
        self.server_socket.listen(self.backlog)

        print('Waiting for bluetooth connection by client...')
        self.client, self.address = self.server_socket.accept()
        print("Accepted connection from", self.address)

    def recv(self):
        return self.client.recv(self.size)

    def send_message(self, message):
        self.client.send(message)

    def reset(self):
        self.client.close()
        self.server_socket.close()
