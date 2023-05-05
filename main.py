import traceback

from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


#TODO: integrate better baro
#TODO: better cut_of by implementing class with algorithm: cut of when to huge change,
#           but accept if second cut of is greater than first. But also get there slowly (maybe not digital filter?)
#TODO: yaw_controller_output goes up when changing from 180 to -180
#TODO: reimplement base euler
#TODO: better algorithm to filter out wrong measurements
#TODO: compensate_orientation is wrong
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
