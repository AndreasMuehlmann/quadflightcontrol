import sys
import pygame

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

class Graph_Repr:
    def __init__(self, width, height):
        self.height = height
        self.width = width

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
            pygame.draw.line(self.window, BLACK, self.center(last), self.center(point))
            last = point

    def draw_target(self):
        if self.target is None:
            return 

        pygame.draw.line(self.window, BLACK, (0, int(-self.target*100 + self.height/2)), (self.width, int(-self.target*100 + self.height/2)))

    def add_point(self, point):
        self.points.append([self.time*100, -point*100])

    def re_draw(self):
        self.window.fill(WHITE)
        self.draw_curve()
        self.draw_target()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.time += 0.01 #an iteration is 10 ms
