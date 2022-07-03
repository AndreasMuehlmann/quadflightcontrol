# Quadrocopter
This is the software used for a quadrocopter in the context of a school project.

The flight control is developed by "Andreas Mühlmann" and hosted on GitHub under:
"https://github.com/AndreasMuehlmann/quadflightcontrol".
There is also a simulation available that is developed by "Felix Ungerhofer" and also hosted on GitHub under:
"https://github.com/AndreasMuehlmann/Drone-Simulation".
An app for user input via bluetooth is developed by "Kilian Schreiner" and also hosted on GitHub under:
"https://github.com/Kilinutz1/Dronenapp".

If you want to use this project, be warned, you have to do most things yourself
primarily if you want to make a real drone.


## Explanation Of The Project's Structure
- The Config: In "config.py" are general settings.
- The Core: "flight_control.py" controls the drone via Controllers and Interfaces.
- The Controllers:
  - They take measurements and the error and return an output, that should be applied to the rotors.
  1. The PidController is a controller from the control-theorie of physiks. It uses static faktors to change it's behavior.
     To get these right you have to manually adjust them in an Environment (more under: "- The Environments:").
     You can inherit from PidController to make a PidController for a specific Environment.
  2. The AdaptivePidController is a PidController with an Deep Reinforcement Learning Agent (sac), that changes the faktors
     so they are not static and there by the AdaptivePidController adapts to other conditions properly.
     The Agent can be trained with "python training.py" .
     - This is a unfinished part of this project and not usable yet.
- The Interfaces: 
  - They either get inputs or apply the output of the controller.
  1. The InterfaceControl collects the measurements and sends the outputs to the rotors:
    1. There is the SimInterface that communicates with the Simulation.
    2. The other Interface is meant to be an Interface to the measuring devices and the actual motors (not working yet).
  2. The InterfaceUser primarily gets the inputs from the user and also sends messages:
    1. There is the BluetoothAppInterface that communicates with the mobile app (not working yet).
    2. There also is the KeyboardInterface.
- The Environments:
  - They are used to test single controllers, give reward for the AdaptivePidController and for
    choosing appropriate faktors for the PidController.
  - Run an episode with "python run_episode.py" and change the faktors for the PidController in the
    config and if they are right and should be used inherit from PidController and make a specialized PidController.
  - You can inherit either from VelEnv, when you control the velocity or from PosEnv, when you control the position (like UnitySimEnv).


## Quickstart
- If you want to use this project you should first read the explanation above, because you will have to do many things yourself.
- Clone the Project with "git clone https://github.com/AndreasMuehlmann/quadflightcontrol.git".
- By running "python main.py" you run the project.

- There are multiple options to set this up:
  1. The Simulation combined with the KeyboardInterface.
  2. The Simulation combined with the BluetoothAppInterface and the Flutter App.
  3. The Raspberry Pi combined with the BluetoothAppInterface and the Flutter App.


### KeyboardInterface
The KeyboardInterface is the easiest way of controlling the drone. Just set it in "interface_user"
in "flight_control.py" to "KeyboardInterface()". This obviously doesn't work for an actual drone.


### Simulation
- Change the interface_control variable to "SimInterface".
- Write the path to where the interface should live, to interfaces/sim_interface_dir_path.txt.

The interface is a folder called interface_sim-control with to files measurements.txt and outputs.txt.
Over those two the programm communicates with the simulation. Then the interface directory is created and
the programm waits for measurements to be written in measurements.txt. As soon as that happens outputs are returned through outputs.txt.

- Now clone the simulation with "git clone https://github.com/AndreasMuehlmann/Drone-Simulation.git".
- For it to read and write properly put the path from the previous interfaces/sim_interface_dir_path.txt in "quadflightcontrol"
  into Assets/sim_interface_dir_path.txt in the just cloned "Drone-Simulation".
- Install Unity.
- Open the project you just cloned.

- Run "python main.py" in "quadflightcontrol", then run the "Drone-Simulation".


### BluetoothAppInterface With Flutter App
This is also still in work but, there is going to be an app, that sends user inputs to
the flight control via bluetooth. Set the "user_interface" in "flight_control.py" to "BluetoothAppInterface()".
You will have to install the app on your mobile phone.


### Raspberry Pi And Solid Actual Quadrocopter
For this you need:
    - sensors
    - batterys
    - motors
    - rotors
    - drone frame
    - raspberry pi

Then you will have to put it all together by making Interfaces to the Motors and the Sensors and a PidController with proper
faktors (you can achieve this by making a proper environmet).

On this path you are quite on your own though...
