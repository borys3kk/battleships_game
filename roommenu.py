import pygame as pg
from constants import *
from button import Button
from onlinegame import OnlineGame


class RoomMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        pg.display.set_caption("Battleships game")
        self.buttons = []
        self.create_screen()
        self.wait_for_click()

    def create_screen(self):
        self.screen.fill((0, 0, 0))
        background = pg.image.load(MENU_IMAGE_PATH)
        background = pg.transform.scale(background, (WIN_SIZE[0] // 3 * 2, WIN_SIZE[1]))
        self.screen.blit(background, (0, 0))

        for i in range(ROOMS):
            button = Button(f"Room {i + 1}", (WIN_SIZE[0]-WIN_SIZE[0]//3)+10, ((WIN_SIZE[1]*i)//5)+10, (255, 255, 255), (WIN_SIZE[0]//3)-20,(WIN_SIZE[1]//5)-20)
            self.buttons.append(button)
            button.draw(self.screen)
        pg.display.update()

    def wait_for_click(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.click(pg.mouse.get_pos()):
                            game = OnlineGame(self.screen)
                            self.running = False

