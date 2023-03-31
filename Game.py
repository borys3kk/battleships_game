import pygame, sys


class Game(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)
