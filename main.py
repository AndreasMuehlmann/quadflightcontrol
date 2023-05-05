import traceback

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


#TODO: compensate_orientation is wrong
#TODO: base_euler keep it or remove it?


def main():
    flight_control = FlightControl()
    try:
        flight_control.run()

    except KeyboardInterrupt:
        flight_control.turn_off()

    except Exception:
        print(traceback.format_exc())
        print('Exception in running flight control')
        flight_control.turn_off()


if __name__ == '__main__':
    main()
