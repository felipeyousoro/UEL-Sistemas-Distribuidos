import pygame
import threading
import time
import random

class WhiteBoard:
    def __init__(self, height=256, width=256, draw_color=(0, 0, 0)):
        pygame.init()
        self.height = height
        self.width = width
        self.draw_color = draw_color
        self.screen = pygame.display.set_mode((height, width))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption('WatanaBoard')
        self.running = True

    def begin(self):
        last_pos = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Desenhar com botão esquerdo do mouse
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    last_pos = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    last_pos = None
                elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                    if last_pos is not None:
                        start_pos = last_pos
                        end_pos = pygame.mouse.get_pos()
                        pygame.draw.line(self.screen, self.draw_color, start_pos, end_pos, 5)
                        last_pos = end_pos

                # Apagar com botão direito do mouse
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    last_pos = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    last_pos = None
                elif event.type == pygame.MOUSEMOTION and event.buttons[2] == 1:
                    if last_pos is not None:
                        start_pos = last_pos
                        end_pos = pygame.mouse.get_pos()
                        pygame.draw.line(self.screen, (255, 255, 255), start_pos, end_pos, 5)
                        last_pos = end_pos

                # Apertar R para cor aleatória
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.draw_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                # Apertar C para limpar a tela
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    self.screen.fill((255, 255, 255))

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    wb = WhiteBoard(512, 512, (255, 0, 0))
    wb.begin()



