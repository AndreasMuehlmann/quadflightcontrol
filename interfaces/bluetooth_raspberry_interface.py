from bluedot.btcomm import BluetoothServer
from signal import pause
from interface_user import InterfaceUser


class BluetoothServerInterface(InterfaceUser):
    Height = float(0)
    Directionx = float(0)
    Directiony = float(0)
    Rotation = float(0)

    def __init__(self):
        s=BluetoothServer(self.data_received)
        

    def give_inputs(self):
        return [self.Height,self.Directionx,self.Directiony,self.Rotation]
        
        #inputs = [float(string_input) for string_input in string_inputs] 

    def data_received(self,data):
        s=data.split()
        if s[0]=="rotation:":
            self.Rotation = float(s[0])
        elif s[0]=="height:":
            self.Height = float(s[1] * -1)
        elif s[0]=="direction:":
            self.Directionx = float(s[1])
            self.Directiony = float(s[2]* -1)

    def send_message(self, message):
        pass

    def reset():
        pass





