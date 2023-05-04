import traceback

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl



#TODO: fix _give_outputs_yaw_controller (rename previous_yaw etc. and add angle_controller_outputs and altitude_controller_output)
#TODO: derivative sometimes seems high => plot pid_controller outputs
#TODO: data_sender doesn't stop when flight_control is reset
#TODO: give_euler function
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
