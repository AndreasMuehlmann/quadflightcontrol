import math
import config as conf
from pid_controller import PidController


class PidFlightControl:
    def __init__(self):
        self.angle_controllers = [PidController(conf.angle_p_faktor, conf.angle_i_faktor,
                                                conf.angle_d_faktor, 300) for _ in range(4)]
        self.yaw_controller = PidController(conf.yaw_p_faktor, conf.yaw_i_faktor,
                                            conf.yaw_d_faktor, 100)
        self.altitude_controller = PidController(conf.altitude_p_faktor, conf.altitude_i_faktor,
                                                 conf.altitude_d_faktor, 600)
        self.rotor_outputs_angle_controllers = [0, 0, 0, 0]
        self.yaw = 0
        self.yaw_controller_output = 0
        self.rotor_outputs_yaw_controller = [0, 0, 0, 0]
        self.altitude_controller_output = 0
        self.rotor_outputs_altitude_controller = [0, 0, 0, 0]

    def give_outputs(self, inputs, rotor_angles, yaw, altitude):
        altitude_difference_target, rotor_angle_targets, yaw_difference_target = inputs

        self.rotor_outputs_angle_controllers = self._give_outputs_angle_controllers(rotor_angle_targets, rotor_angles)
        self.rotor_outputs_yaw_controller = self._give_outputs_yaw_controller(yaw_difference_target, yaw)
        self.rotor_outputs_altitude_controller = self._give_outputs_altitude_controller(altitude_difference_target, altitude)
        # self.altitude_controller_output = self._compensate_orientation_in_vertical_acc(self.altitude_controller_output,
        #                                                                            rotor_angles[0], rotor_angles[1])
        outputs = [rotor_output_altitude_controller + rotor_output_angle_controller + rotor_output_yaw_controller \
                   for rotor_output_angle_controller, rotor_output_yaw_controller, rotor_output_altitude_controller \
                   in zip(self.rotor_outputs_angle_controllers, self.rotor_outputs_yaw_controller, self.rotor_outputs_altitude_controller)]
        outputs = self._remove_negatives(outputs)
        outputs = self._remove_over_max_output(outputs)
        return outputs

    def _give_outputs_angle_controllers(self, rotor_angle_targets, rotor_angles):
        self.rotor_outputs_angle_controllers = []
        for rotor_angle, rotor_angle_target, angle_controller in \
                zip(rotor_angles, rotor_angle_targets, self.angle_controllers):
            self.rotor_outputs_angle_controllers.append(angle_controller.give_output(rotor_angle_target - rotor_angle, rotor_angle))
        return self.rotor_outputs_angle_controllers

    def _give_outputs_yaw_controller(self, yaw_difference_target, yaw):
        changed_negativ_positiv = (yaw > 170 and self.yaw < -170) \
            or (yaw < -170 and self.yaw > 170)
        if changed_negativ_positiv:
            return self.rotor_outputs_yaw_controller
        self.yaw_controller_output = self.yaw_controller \
            .give_output(yaw + yaw_difference_target, yaw)
        self.rotor_outputs_yaw_controller = [-self.yaw_controller_output, self.yaw_controller_output,
                                             -self.yaw_controller_output, self.yaw_controller_output]
        self.yaw = yaw
        return self.rotor_outputs_yaw_controller

    def _give_outputs_altitude_controller(self, altitude_difference_target, altitude, rotor_angles):
        self.altitude_controller_output = self.altitude_controller \
            .give_output(altitude + altitude_difference_target, altitude)
        return [self.altitude_controller_output for _ in range(4)]

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
        self.yaw_controller.reset()
