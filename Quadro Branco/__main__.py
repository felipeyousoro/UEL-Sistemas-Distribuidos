import pygame
import threading
import time
import random


class Circle:
    def __init__(self, x: float, y: float, r: float, width: int, color: (int, int, int)):
        self.x = x
        self.y = y
        self.r = r
        self.width = width
        self.color = color

    def isPointInside(self, x: float, y: float) -> bool:
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.r ** 2


class WhiteBoard:
    def __init__(self, height=256, width=256, draw_color=(0, 0, 0)):
        pygame.init()

        self.height = height
        self.width = width

        self.draw_color = draw_color

        self.screen = pygame.display.set_mode((height, width))

        pygame.display.set_caption('WatanaBoard')

        self.running = True

        self.circles: list[Circle] = []

    def begin(self):
        active_circle = -1

        while self.running:
            self.screen.fill((255, 255, 255))

            for circle in self.circles:
                pygame.draw.circle(self.screen, circle.color, (circle.x, circle.y), circle.r, width=circle.width)

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
                            self.circles.append(Circle(position[0], position[1], 20, 5, self.draw_color))
                    elif event.button == 3:
                        for num, circle in enumerate(self.circles):
                            if circle.isPointInside(position[0], position[1]):
                                self.circles.pop(num)
                                break

                if event.type == pygame.MOUSEMOTION:
                    position = pygame.mouse.get_pos()
                    if active_circle != -1:
                        self.circles[active_circle].x = position[0]
                        self.circles[active_circle].y = position[1]

                if event.type == pygame.MOUSEBUTTONUP:
                    active_circle = -1

        pygame.quit()


if __name__ == '__main__':
    wb = WhiteBoard(512, 512, (255, 0, 0))
    wb.begin()
