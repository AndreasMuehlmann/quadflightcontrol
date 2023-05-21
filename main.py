import traceback

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


#TODO: make tests and tune PID-Controllers
#TODO: use PI-Controller / PID-Controller for Yaw and PD-Controller for angle and PID-Controller for altitude
#TODO: make a take-off phase
#TODO: build models for altitude yaw, altitude, roll, pitch from logged data
#TODO: improve recv_data
#TODO: resetting measurement
#TODO: edge cases like app turning off
#TODO: get the simulation to work again
#TODO: improve the README


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
