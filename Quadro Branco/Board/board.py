import random

import pygame

from Circle import circle as c
from Connection import connection as conn

class Board:
    def __init__(self, connection: conn.Connection, height=256, width=256, draw_color=(255, 0, 0)):
        pygame.init()

        self.height = height
        self.width = width

        self.draw_color = draw_color

        self.screen = pygame.display.set_mode((height, width))

        pygame.display.set_caption('WatanaBoard')
        clock = pygame.time.Clock().tick(30)

        self.running = True

        self.connection = connection
        self.circles = self.connection.database.circles

    def begin(self):
        active_circle = -1

        while self.running:
            self.screen.fill((255, 255, 255))

            for circle in self.circles:
                pygame.draw.circle(self.screen, circle.color, (circle.x, circle.y), circle.r, width=circle.width)
                # print(circle.x, circle.y, circle.r, circle.width, circle.color)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.draw_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if event.button == 1:
                        for num, circle in enumerate(self.circles):
                            if circle.isPointInside(position[0], position[1]):
                                # if circle.lock_holder == -1:
                                #     if pygame.key.get_mods() & pygame.KMOD_CTRL:
                                #         circle.r += 5
                                #         circle.width += 1
                                #     elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                #         circle.r -= 5
                                #         circle.width -= 1
                                active_circle = num
                                break
                        else:
                            self.connection.request_add_circle(c.Circle(0, position[0], position[1], 30, 7, self.draw_color))
                    elif event.button == 3:
                        for num, circle in enumerate(self.circles):
                            if circle.isPointInside(position[0], position[1]):
                                print(f'Requesting lock/unlock for circle {circle.id}')
                                if circle.lock_holder == -1:
                                    self.connection.request_lock_circle(circle)
                                    print('(!) > Lock accept')
                                elif circle.lock_holder == self.connection.port:
                                    self.connection.request_unlock_circle(circle)
                                    print('(!) > Unlock accept')
                                else:
                                    print(f'(!) > Lock reject, circle {circle.id} is locked by {circle.lock_holder}')
                                break

                if event.type == pygame.MOUSEMOTION:
                    if active_circle != -1:
                        position = pygame.mouse.get_pos()
                        self.connection.request_move_circle(self.circles[active_circle], position[0], position[1])

                if event.type == pygame.MOUSEBUTTONUP:
                    active_circle = -1

        pygame.quit()

    def set_circles(self, circles: list[c.Circle]):
        self.circles = circles