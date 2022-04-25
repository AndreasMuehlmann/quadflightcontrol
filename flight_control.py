from transform_input import give_heights
from adaptive_pid_controller import pid_controller as pid

'''
(fl) rotor2 -> \ / <- rotor1 (fr)
                °
(bl) rotor3 -> / \ <- rotor4 (br)

[rotor1, rotor2, rotor2, rotor4]
'''

class FlightControl:

    def __init__(self, x, y, pos):
        heights = give_heights(x, y)
        self.pid_controllers = map(lambda height : pid.PidController(height - pos, pos), heights)

    def input_to_rpm(self, x, y, strength, pos): # pos has to be changed to angel later
        #height and pos is relativ to the center of the Drone
        heights = give_heights(x, y)

        rpm = []
        for count, pid_controller in enumerate(self.pid_controllers):
            rpm.append(pid_controller.give_output(heights[count] - pos[count], pos[count]) + strength)

        return rpm