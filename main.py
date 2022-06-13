from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


def main():
    flight_contorl = FlightControl()
    flight_contorl.run()


if __name__ == '__main__':
    main()
