import math
import config as conf
from pid_controller import PidController


class PidFlightControl:
    def __init__(self):
        self.angle_controllers = [PidController(conf.angle_p_faktor, conf.angle_i_faktor,
                                                conf.angle_d_faktor, 50) \
                                                        for _ in range(4)]
        self.rotation_controller = PidController(conf.rotation_p_faktor, conf.rotation_i_faktor,
                                                conf.rotation_d_faktor, 500)
        self.height_vel_controller = PidController(conf.height_vel_p_faktor, conf.height_vel_i_faktor,
                                                conf.height_vel_d_faktor, 600)
        

    def give_outputs(self, inputs, rotor_angles, rotation, height_vel):
        height_vel_target, rotor_angle_targets, rotation_target = inputs

        angle_controller_outputs = self._give_outputs_angle_controllers(rotor_angle_targets, rotor_angles)
        rotation_controller_outputs = self._give_outputs_rotation_controller(rotation_target, rotation)
        print([round(o, 2) for o in rotation_controller_outputs])
        height_vel_controller_output = self.height_vel_controller.give_output(height_vel_target - height_vel, height_vel)
        # height_vel_controller_output = self._compensate_orientation_in_vertical_acc(height_vel_controller_output,
        #                                                                            rotor_angles[0], rotor_angles[1])
        outputs = [height_vel_controller_output +  angle_controller_output + rotation_controller_output \
                for angle_controller_output, rotation_controller_output in zip(angle_controller_outputs, rotation_controller_outputs)]
        outputs = self._remove_negatives(outputs)
        outputs = self._remove_over_max_output(outputs)
        return outputs

    def _give_outputs_angle_controllers(self, rotor_angle_targets, rotor_angles):
        outputs = []
        for rotor_angle, rotor_angle_target, angle_controller in \
        zip(rotor_angles, rotor_angle_targets, self.angle_controllers):
            outputs.append(angle_controller.give_output(rotor_angle_target - rotor_angle, rotor_angle))
        return outputs

    def _give_outputs_rotation_controller(self, rotation_target, rotation):
        output = self.rotation_controller.give_output(rotation_target - rotation, rotation)
        return [-output, output, -output, output]

    def _compensate_orientation_in_vertical_acc(self, base_output, roll, pitch):
        # sin(alpha) = horizontal_acc / base_output
        # horizontal_acc = sin(alpha) * base_output
        print(math.sin(abs(roll) + abs(pitch)))
        return math.sin((abs(roll) + abs(pitch)) / 360 * 2*math.pi) * base_output

    def _remove_negatives(self, outputs):
        new_outputs = []
        for output in outputs: 
            if output < 0:
                output = 0
            new_outputs.append(output)
        return new_outputs

    def _remove_over_max_output(self, outputs):
        new_outputs = []
        for output in outputs: 
            if output > conf.max_output:
                output = conf.max_output
            new_outputs.append(output)
        return new_outputs

    def reset(self):
        for angle_controller in self.angle_controllers:
            angle_controller.reset()
        self.rotation_controller.reset()
