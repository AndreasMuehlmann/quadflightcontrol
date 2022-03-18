import random
import time
import sys
import pygame

from pid_controller import give_rpm

HEIGHT = 1300
WIDTH = 2500

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

def center(point):
    return (int(point[0]), int(point[1] + HEIGHT/2))

def draw_curve(points):
    if not points:
        return

    last = points[0]
    for point in points[1:]:
        pygame.draw.line(window, BLACK, center(last), center(point))
        last = point

def draw_target(target):
    pygame.draw.line(window, BLACK, (0, int(-target*100 + HEIGHT/2)), (WIDTH, int(-target*100 + HEIGHT/2)))

def main():
    global window

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f'y: pos, x: time')

    last_time = time.time()

    pos = 0
    vel = 0
    acc = 0

    last_acc = 0
    last_vel = 0

    target = 1

    randomize_start = 0
    test_start = time.time()

    points = []
    while True:
        window.fill(WHITE)
        draw_target(target)
        draw_curve(points)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (time.time() - test_start) > 0 and time.time() - randomize_start > 100:
            randomize_start = time.time()
            if random.randint(0, 1) == 1:
                target -= random.random() * 0.1
            else:
                target += random.random() * 0.1


        delta_time = time.time() - last_time
        last_time = time.time()

        rpm = give_rpm(target - pos)

        acc += rpm * 0.1
        vel += (acc + last_acc) / 2 * delta_time
        pos += (vel + last_vel) / 2 * delta_time
        #print(f'pos: {round(pos, 2)}, vel: {round(vel, 2)}, acc: {round(acc, 2)}, total_time: {round(time.time() - test_start, 4)}')

        points.append([(time.time() - test_start) * 100, -pos*100])

        last_acc = acc
        last_vel = vel

    pygame.quit()

if __name__ == '__main__':
    main()