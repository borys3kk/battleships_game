from Game import Game
import pygame as pg
from wrapper import Wrapper

WIN_SIZE = (1280, 720)
MENU_IMAGE_PATH = 'assets/backgrounds/Battleship.jpg'

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption("Battleships game")
    background = pg.image.load(MENU_IMAGE_PATH)
    background = pg.transform.scale(background,(WIN_SIZE[0]//3*2,WIN_SIZE[1]))
    button = pg.image.load('assets/button.png')
    button = pg.transform.scale(button,(WIN_SIZE[0]//3,WIN_SIZE[0]//3))
    button_rect = button.get_rect()
    button_width = button.get_width()
    button_rect.center = (WIN_SIZE[0] - button_width//2,WIN_SIZE[1]//2)
    screen.blit(background,(0,0))
    screen.blit(button,button_rect)
    pg.display.update()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(pg.mouse.get_pos()):
                    game = Game(screen)
                    running = False

