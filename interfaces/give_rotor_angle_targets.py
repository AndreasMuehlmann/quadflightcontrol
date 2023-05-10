from math import pi, atan, sqrt

import config as conf

'''
  rotor2 -> |
rotor3 -> - ° - <- rotor1
            | <- rotor4

[rotor1, rotor2, rotor3, rotor4]
'''

def give_rotor_angle_targets(x, y):
    radius = _give_radius(x, y)
    if radius == 0:
        return [0, 0]

    angle_drone = radius * conf.max_angle_drone
    angle_alpha =  _calc_angle(x, y)
    circular_arc = _give_circular_arc(angle_alpha, radius)
    part_90_degree_circular_arc = _give_circular_arc(angle_alpha, radius) \
        / _give_circular_arc(90, radius)
    other_part = 1 - part_90_degree_circular_arc

    angle_rotor_horiz = (1 - part_90_degree_circular_arc) * angle_drone
    angle_rotor_verti = (1 - other_part) * angle_drone

    if x >= 0:
        if y >= 0:
            angles = [-angle_rotor_horiz, -angle_rotor_verti]

        if y <= 0:
            angles = [-angle_rotor_horiz, angle_rotor_verti]

    if x <= 0:
        if y >= 0:
            angles = [angle_rotor_horiz, -angle_rotor_verti]

        if y <= 0:
            angles = [angle_rotor_horiz, angle_rotor_verti]

    return angles


def _give_radius(x, y):
    return sqrt(x ** 2 + y ** 2)


def _calc_angle(x, y):
    if x == 0:
        return 90

    angle = atan(y / x) / (2 * pi) * 360 # converted to degrees
    return abs(angle)


def _give_circular_arc(angle, radius):
    return angle / 360 * 2 * pi * radius
