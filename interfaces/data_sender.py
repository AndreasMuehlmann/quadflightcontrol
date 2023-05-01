import time
import zmq


class DataSender:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5555")
    
    def send_message(self, data):
        self.socket.send_string('flight_data:' + data)

    def reset(self):
        self.context.destroy()
