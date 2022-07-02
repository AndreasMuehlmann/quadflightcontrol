from append_dirs_to_path import append_dirs_to_path
append_dirs_to_path()

from flight_control import FlightControl


# TODO: make better names
# TODO: mark private methods
# TODO: write documentation
# TODO: make a .gitignore
# TODO: adjust values to UnitySim
# TODO: print reward afer run_episode
# TODO: everything with init (no init_values) call super init in the end for default values
# TODO: should_reset into controller env
# TODO: make pid_controller faktor adjust to environment (inherit from pid_controller)
# TODO: fix transform_inputs
# TODO: make default values in PosEnv
# TODO: maybe remove self.faktor from self.env_force
# TODO: make drone stay on same height when tilted
#

def main():
    flight_control = FlightControl()
    flight_control.run()


if __name__ == '__main__':
    main()
