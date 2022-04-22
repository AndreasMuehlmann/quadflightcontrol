import sys
import pygame

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

class GraphRepr:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        
        self.y_stretch = 50
        self.x_stretch = 100

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f'y: pos, x: time')

        self.points = []
        self.target = None
        self.time = 0 #in s

    def center(self, point):
        return (int(point[0]), int(point[1] + self.height/2))

    def draw_curve(self):
        if not self.points:
            return

        last = self.points[0]
        for point in self.points[1:]:
            pygame.draw.line(self.window, BLACK, (last[0] * self.x_stretch, -last[1] * self.y_stretch + self.height / 2), (point[0] * self.x_stretch, -point[1] * self.y_stretch + self.height / 2))
            last = point

    def draw_target(self):
        if self.target is None:
            return 

        self.y_stretch = self.get_stretch(9 * self.height / 20, self.target, self.y_stretch)
        pygame.draw.line(self.window, BLACK, (0, int(-self.target * self.y_stretch + self.height / 2)), (self.width, int(-self.target * self.y_stretch + self.height / 2)))

    def add_point(self, point):
        self.y_stretch = self.get_stretch(9 * self.height / 20, point, self.y_stretch)
        self.x_stretch = self.get_stretch(9 * self.width / 10, self.time, self.x_stretch)
        self.points.append([self.time, point])

    def get_stretch(self, stretch_to, val, stretch):
        # 9 * window_length / (10 * 2) = stretch * max_val
        if val == 0:
            return stretch

        new_stretch = stretch_to / abs(val)
        return new_stretch if new_stretch < stretch else stretch

    def re_draw(self):
        self.window.fill(WHITE)
        self.draw_target()
        self.draw_curve()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.time += 0.01 #an iteration is 10 ms
