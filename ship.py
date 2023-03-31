from wrapper import Wrapper
import pygame as pg


class Ship(Wrapper):
    def __init__(self, name, path, top_left, size):
        super().__init__()
        self.name = name
        self.active = False
        self.top_left = top_left
        self.v_image = self.load_image(path, size)
        self.v_image_rect = self.v_image.get_rect()
        self.v_image_rect.topleft = self.top_left

    def load_image(self, path, size: tuple((int, int)), rotate=False):
        return super().load_image(path, size, rotate)

    def draw(self, screen):
        screen.blit(self.v_image, self.v_image_rect)

    def drag_ship(self,game):
        while self.active:
            self.v_image_rect.center = pg.mouse.get_pos()
            print(self.v_image_rect.center)
            game.update_screen()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    self.active = False
                    return
