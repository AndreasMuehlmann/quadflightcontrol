import bluetooth


class BluetoothClient(InterfaceUser):
    def __init__(self):
        self.hostMACAddress = '' # MAC-Address of Raspberry Pi
        self.port = 3
        self.backlog = 1
        self.size = 1024
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.bind((hostMACAddress, port))
        self.socket.listen(backlog)
        try:
            self.client, self.clientInfo = self.socket.accept()
        except:
            self.reset()

    def give_inputs(self):
        try:
            data = client.recv(size)
        except:
            self.reset()

        return [200, 0, 0, 0]

    def send_message(self, message):
        client.send(message)

    def reset():
        self.client.close()
        self.socket.close()
