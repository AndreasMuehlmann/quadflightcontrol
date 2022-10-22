from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


#TODO: make pid_controller faktor adjust to environment (inherit from pid_controller)
#TODO: watchout because angle lets drone behave weird
#TODO: unity_sim_env is not like unity simulation
#TODO: also look in training.py for TODOS
#TODO: make a sequence diagramm and put it in the README
#TODO: add videos for the simulation and maybe also for the actual drone
#TODO: low priority: make drone stay on same height when tilted


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
