import traceback

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


#TODO: give yaw sometimes doesn't work right
#TODO: change everything from height_vel to altitude
#TODO: change everything from rotation to yaw
#TODO: compensate_orientation is wrong


def main():
    flight_control = FlightControl()
    try:
        flight_control.run()

    except KeyboardInterrupt:
        flight_control.reset()

    except Exception as e:
        print(traceback.format_exc())
        print('Exception in running flight control')
        flight_control.reset()


if __name__ == '__main__':
    main()
