import pygame
import sys

from interface_user import InterfaceUser


class KeyboardInterface(InterfaceUser):
    def __init__(self):
        pygame.init()
        display = pygame.display.set_mode((300, 300))

        self.base_output = 0
        self.pressed = {'w': False, 's': False, 'a': False, 'd': False, 'UP': False,
                        'DOWN': False, 'LEFT': False, 'RIGHT': False}

    def _update_pressed_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pressed['UP'] = True

                if event.key == pygame.K_DOWN:
                    self.pressed['DOWN'] = True

                if event.key == pygame.K_LEFT:
                    self.pressed['LEFT'] = True

                if event.key == pygame.K_RIGHT:
                    self.pressed['RIGHT'] = True

                if event.key == pygame.K_w:
                    self.pressed['w'] = True

                if event.key == pygame.K_d:
                    self.pressed['d'] = True

                if event.key == pygame.K_a:
                    self.pressed['a'] = True

                if event.key == pygame.K_s:
                    self.pressed['s'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.pressed['UP'] = False

                if event.key == pygame.K_DOWN:
                    self.pressed['DOWN'] = False

                if event.key == pygame.K_LEFT:
                    self.pressed['LEFT'] = False

                if event.key == pygame.K_RIGHT:
                    self.pressed['RIGHT'] = False

                if event.key == pygame.K_w:
                    self.pressed['w'] = False

                if event.key == pygame.K_s:
                    self.pressed['s'] = False

                if event.key == pygame.K_a:
                    self.pressed['a'] = False

                if event.key == pygame.K_d:
                    self.pressed['d'] = False


    def give_inputs(self):
        self.strength_x_slope = 0
        self.strength_y_slope = 0
        self.rotation_vel = 0

        self._update_pressed_keys()

        if self.pressed['UP']:
            self.strength_y_slope += 0.3

        if self.pressed['DOWN']:
            self.strength_y_slope -= 0.3

        if self.pressed['LEFT']: 
            self.strength_x_slope -= 0.3

        if self.pressed['RIGHT']:
            self.strength_x_slope += 0.3

        if self.pressed['w']:
            self.base_output += 0.1

        if self.pressed['s']:
            self.base_output -= 0.1

        if self.pressed['a']:
            self.rotation_vel -= 0.1

        if self.pressed['d']:
            self.rotation_vel += 0.1

        if self.base_output < 0:
            self.base_output = 0

        if self.base_output > conf.max_output:
            self.base_output = conf.max_output

        return self.base_output, self.strength_x_slope, self.strength_y_slope, self.rotation_vel

    def send_outputs(self, outputs):
        pass
