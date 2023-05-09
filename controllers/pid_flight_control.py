import numpy as np
import config as conf
from pid_controller import PidController


class PidFlightControl:
    def __init__(self):
        self.angle_controllers = [PidController(conf.angle_p_faktor, conf.angle_i_faktor,
                                                conf.angle_d_faktor, 300, 50) for _ in range(2)]
        self.yaw_controller = PidController(conf.yaw_p_faktor, conf.yaw_i_faktor,
                                            conf.yaw_d_faktor, 200, 100)
        self.altitude_controller = PidController(conf.altitude_p_faktor, conf.altitude_i_faktor,
                                                 conf.altitude_d_faktor, 600, 500)
        self.yaw_target = 0
        self.altitude_target = 0
        self.rotor_outputs_angle_controllers = [0, 0, 0, 0]
        self.yaw = 0
        self.yaw_controller_output = 0
        self.rotor_outputs_yaw_controller = [0, 0, 0, 0]
        self.altitude_controller_output = 0
        self.rotor_outputs_altitude_controller = [0, 0, 0, 0]

    def give_outputs(self, inputs, rotor_angles, yaw, altitude):
        altitude_difference_target, rotor_angle_targets, yaw_difference_target = inputs
        self.yaw_target += yaw_difference_target / conf.frequency
        self.altitude_target += altitude_difference_target / conf.frequency

        self.rotor_outputs_angle_controllers = self._give_outputs_angle_controllers(rotor_angle_targets, rotor_angles)
        self.rotor_outputs_yaw_controller = self._give_outputs_yaw_controller(self.yaw_target, yaw)
        self.rotor_outputs_altitude_controller = self._give_outputs_altitude_controller(self.altitude_target, altitude)
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
        return self.rotor_outputs_angle_controllers.extend(
                [-self.rotor_outputs_angle_controllers[0] + -self.rotor_outputs_angle_controllers[0]])

    def _give_outputs_yaw_controller(self, yaw_target, yaw):
        changed_negativ_positiv = (yaw > 170 and self.yaw < -170) \
            or (yaw < -170 and self.yaw > 170)
        if changed_negativ_positiv:
            self.yaw_controller.give_output(yaw - yaw_target, yaw)
            self.yaw = yaw
            return self.rotor_outputs_yaw_controller
        self.yaw_controller_output = self.yaw_controller \
            .give_output(yaw - yaw_target, yaw)
        self.rotor_outputs_yaw_controller = [-self.yaw_controller_output, self.yaw_controller_output,
                                             -self.yaw_controller_output, self.yaw_controller_output]
        self.yaw = yaw
        return self.rotor_outputs_yaw_controller

    def _give_outputs_altitude_controller(self, altitude_target, altitude):
        self.altitude_controller_output = self.altitude_controller \
            .give_output(-altitude + altitude_target, altitude)
        return [self.altitude_controller_output for _ in range(4)]

    def _compensate_orientation_in_vertical_acc(self, altitude_output, roll, pitch):
        unit_vektor_roll = np.array([np.cos(roll), 0, np.sin(roll)])
        unit_vektor_pitch = np.array([0, np.cos(pitch), np.sin(pitch)])
        n_vektor = np.cross(unit_vektor_roll, unit_vektor_pitch)
        unit_n_vektor = n_vektor / np.linalg.norm(n_vektor)
        angle_quadcopter_plane_to_x1_x2_plane = np.arccos(np.dot(np.array([0, 0, 1]), unit_n_vektor))
        print(f'{angle_quadcopter_plane_to_x1_x2_plane}, {altitude_output}, {altitude_output / np.cos(angle_quadcopter_plane_to_x1_x2_plane)}')
        return altitude_output / np.cos(angle_quadcopter_plane_to_x1_x2_plane)

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
