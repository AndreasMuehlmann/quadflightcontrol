import sys

import pygame

import config as conf


WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)


class GraphRepr:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        
        self.x_stretch = conf.default_x_stretch
        self.y_stretch = conf.default_y_stretch

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f'Graph')

        self.points = []
        self.target = None

        self.size_coordinate_system_markers = 10

    def _draw_curve(self):
        if not self.points:
            return

        last = self.points[0]
        for point in self.points[1:]:
            pygame.draw.line(self.window, BLACK,
                             (last[0] * self.x_stretch, -last[1] * self.y_stretch + self.height / 2),
                             (point[0] * self.x_stretch, -point[1] * self.y_stretch + self.height / 2))
            last = point

    def _draw_target(self):
        if self.target is None:
            return 

        self.y_stretch = self._get_stretch(9 * self.height / 20, self.target, self.y_stretch)
        pygame.draw.line(self.window, BLACK, (0, int(-self.target * self.y_stretch + self.height / 2)), (self.width, int(-self.target * self.y_stretch + self.height / 2)))

    def _draw_coordinate_system(self):
        for pixel in range(0, self.width, conf.x_dist_coord_sys):
            pygame.draw.line(self.window, BLACK,
                             (int(pixel * self.x_stretch), self.height),
                             (int(pixel * self.x_stretch), self.height - self.size_coordinate_system_markers))

        for pixel in range(0, self.height, conf.y_dist_coord_sys):
            pygame.draw.line(self.window, BLACK,
                             (self.width, int(pixel * self.y_stretch)),
                             (self.width - self.size_coordinate_system_markers, int(pixel * self.y_stretch)))

        pygame.draw.line(self.window, BLACK,
                         (self.width, int(self.height / 2)),
                         (self.width - self.size_coordinate_system_markers * 4, int(self.height / 2)))



    def add_point(self, time, point):
        self.y_stretch = self._get_stretch(9 * self.height / 20, point, self.y_stretch)
        self.x_stretch = self._get_stretch(9 * self.width / 10, time, self.x_stretch)
        self.points.append([time, point])

    def _get_stretch(self, stretch_to, val, stretch):
        # 9 * window_length / (10 * 2) = stretch * max_val
        if val == 0:
            return stretch

        new_stretch = stretch_to / abs(val)
        return new_stretch if new_stretch < stretch else stretch

    def update(self):
        self.window.fill(WHITE)
        self._draw_target()
        self._draw_curve()
        self._draw_coordinate_system()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
