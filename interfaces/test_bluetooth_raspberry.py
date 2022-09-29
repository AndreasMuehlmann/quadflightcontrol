from bluetooth_raspberry_interface import BluetoothRaspberryInterface

def main():
    bri = BluetoothRaspberryInterface()

    while True:
        inputs = bri.give_inputs()
        print(inputs)
        

if __name__ == '__main__':
    main()
