from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


#TODO: rotation from pos not vel
#TODO: altitude from pos not vel
#TODO: compensate_orientation is wrong


def main():
    flight_control = FlightControl()
    try:
        flight_control.run()

    except KeyboardInterrupt:
        flight_control.reset()

    except Exception as e:
        print(e)
        print('Exception in running flight control')
        flight_control.reset()


if __name__ == '__main__':
    main()
