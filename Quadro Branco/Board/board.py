import random

import pygame

from Circle import circle as c
from Connection import connection as conn

class Board:
    def __init__(self, connection: conn.Connection, height=256, width=256, draw_color=(0, 0, 0)):
        pygame.init()

        self.height = height
        self.width = width

        self.draw_color = draw_color

        self.screen = pygame.display.set_mode((height, width))

        pygame.display.set_caption('WatanaBoard')

        self.running = True

        self.circles: list[c.Circle] = []

        self.connection = connection

    def begin(self):
        active_circle = -1

        while self.running:
            self.screen.fill((255, 255, 255))

            for circle in self.circles:
                pygame.draw.circle(self.screen, circle.color, (circle.x, circle.y), circle.r, width=circle.width)
                #print(circle)

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
                            if circle.isPointInside(position[0], position[1]) and not circle.locked:
                                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                                    circle.r += 5
                                    circle.width += 1
                                elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                    circle.r -= 5
                                    circle.width -= 1
                                else:
                                    active_circle = num
                                break
                        else:
                            self.circles.append(c.Circle(0, position[0], position[1], 20, 5, self.draw_color))
                    elif event.button == 3:
                        for num, circle in enumerate(self.circles):
                            if circle.isPointInside(position[0], position[1]) and not circle.locked:
                                self.circles.pop(num)
                                break

                if event.type == pygame.MOUSEMOTION:
                    position = pygame.mouse.get_pos()
                    if active_circle != -1:
                        self.circles[active_circle].x = position[0]
                        self.circles[active_circle].y = position[1]
                        self.circles[active_circle].locked = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if(active_circle != -1):
                        self.circles[active_circle].locked = False
                    active_circle = -1

        pygame.quit()

    def setCircles(self, circles: list[c.Circle]):
        self.circles = circles