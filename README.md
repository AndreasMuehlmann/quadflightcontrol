# Drone
This is the software used for a drone. To be more specific a quadrocopter.

It is mainly developed by Andreas Mühlmann and hosted on GitHub under: https://github.com/AndreasMuehlmann/Drone.
There is also a simulation available that is developed by Felix Ungerhofer and also hosted
on GitHub under: https://github.com/AndreasMuehlmann/Drone-Simulation.
An app for user input via Bluetooth is developed by Kilian Schreiner.

If you want to use this Project be warned, you have to change everything yourself in 
the code and the project also is unstable and unfinished.


# Quickstart:
- Clone the Project with 'git clone https://github.com/AndreasMuehlmann/Drone'.

You can then use the Project for maybe a raspberry pi and try controlling a drone with it,
or you control the simulation.

## Simulation:
- Change the interface_control variable to 'SimInterface' (you might have to import it from 'interface/sim_interface.py')
- Write the path to where the interface should live, to interfaces/sim_interface_dir_path.txt.

The interface is a folder called interface_sim-control with to files measurements.txt and outputs.txt.
Over those two the programm communicates with the simulation.

- Run the programm with 'python main.py'.

Then the interface directory is created and the programm waits for measurements to be written in measurements.txt.
As soon as that happens outputs are returned through outputs.txt.

- Now clone the simulation with 'git clone https://github.com/AndreasMuehlmann/Drone-Simulation'

To run it, you have to have Unity installed. The Simulation has to read from the interface and
then you hopefully see the drone flying.

## Raspberry Pi:
This is still in work, but technically you need a sensor with a raspberry pi and then you can
try and make it work.

## Bluetooth Control With Flutter App
This is also still in work but, there is going to be an app, that sends user inputs to
the flight control. This is going to be in 'interfaces/bluetooth_interface.py'

