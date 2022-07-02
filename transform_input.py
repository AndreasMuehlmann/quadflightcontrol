from math import pi, atan, sqrt

'''
rotor2 -> \ / <- rotor1
           °
rotor3 -> / \ <- rotor4

[rotor1, rotor2, rotor2, rotor4]
'''

def give_heights(x, y):
    radius = _give_radius(x, y) * 1
    if radius == 0:
        return [0, 0, 0, 0]
    
    if  abs(y) > 0 or abs(x) > 0:
        angle =  _calculate_angle(x, y)

        if angle == None:
            distance = 1/8 * pi 
            hr, hl = _calculate_heights(distance, distance, radius)   

            #center_low
            if y < 0:
                angle = 270
                return [hr,hr,-hr, -hr]

            #center_high
            else:
                angle = 90
                return [-hr,-hr,hr,hr]

        #top quarter
        if angle < 135 and angle >= 45:
            distance_right = (angle - 45) / 360 *  pi #to 1
            distance_left =  (135 - angle) / 360 *  pi #to 2

            height_right, height_left = _calculate_heights(distance_right, distance_left, radius)
            return [-height_right, -height_left, height_right, height_left]

        #left quarter
        elif angle < 225 and angle >= 135:
            distance_right = (angle - 135) / 360  * pi #to 2
            distance_left =  (225 - angle) / 360 * pi #to 3

            height_right, height_left = _calculate_heights(distance_right, distance_left, radius)
            return [height_left, -height_right, -height_left, height_right]

        #bottom quarter
        elif angle < 315 and angle >= 225:
            distance_right = (angle-225)/360  * pi #to 3
            distance_left =  (315-angle)/360  * pi #to 4

            height_right,height_left = _calculate_heights(distance_right,distance_left,radius)
            return [height_right,height_left,-height_right, -height_left]

        #right quarter
        else:
            if angle >= 45:
                distance_right = (angle - 315) / 360 * pi #to 4
                distance_left =  (360 - angle + 45) / 360  * pi #to 1

            else:
                distance_right = (angle + 45) / 360 * pi #to 4
                distance_left =  (45 - angle) / 360  * pi #to 1

            height_right, height_left = _calculate_heights(distance_right, distance_left, radius)

            return [-height_left,height_right,height_left, -height_right]

def _calculate_angle(x, y):
    if x == 0:
        return None

    angle = (atan(y / x)) / (2 * pi) * 360 
    if x < 0:
        return  angle + 180
        
    if angle < 0:
        return  angle + 360

def _give_radius(x, y):
    return sqrt(x*x + y*y)

def _calculate_heights(x, y, abweichung):
    return abweichung * (1/4 * pi - x), abweichung * (1/4 * pi - y)


if __name__ == "__main__":
    print(give_heights(-1, 0))
