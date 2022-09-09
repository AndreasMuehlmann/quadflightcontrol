from bluetooth_server_interface import BluetoothServerInterface


def main():
    bluetooth_server_interface = BluetoothServerInterface()
    try:
        while True:
            print(give_inputs())
    except KeyboardInterrupt:
        bluetooth_server_interface.reset()


if __name__ == '__main__':
    main()
