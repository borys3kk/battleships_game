from wrapper import Wrapper
import pygame as pg
from grid import Grid


class Ship(Wrapper):
    def __init__(self, name, path, top_left, size, ship_length):
        super().__init__()
        self.name = name
        self.active = False
        self.top_left = top_left
        self.v_image = self.load_image(path, size)
        self.v_image_rect = self.v_image.get_rect()
        self.v_image_rect.topleft = self.top_left
        self.h_image = pg.transform.rotate(self.v_image, -90)
        self.h_image_rect = self.h_image.get_rect()
        self.h_image_rect.topleft = top_left
        self.image = self.v_image
        self.image_rect = self.v_image_rect
        self.rotated = False
        self.no_hits = 0
        self.ship_length = ship_length
        self.placed = False

        self.destroyed = False
    
    def load_image(self, path, size: tuple((int, int)), rotate=False):
        return super().load_image(path, size, rotate)

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)

    def handle_shot(self):
        self.no_hits += 1
        print(self.no_hits, self.ship_length)
        self.destroyed = self.no_hits == self.ship_length


    def drag_ship(self, game):
        while self.active:
            self.image_rect.center = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.rotate_ship()
                elif event.type == pg.MOUSEBUTTONUP:
                    if not self.check_for_collisions(game.fleet):
                        self.h_image_rect.center = self.v_image_rect.center = self.image_rect.center
                        self.placed = True
                    else:
                        self.default_position()
                        self.placed = False
                    self.active = False
                game.update_screen()
            game.update_screen()

    def rotate_ship(self):
        if self.rotated:
            self.image = self.v_image
            self.image_rect = self.v_image_rect
        else:
            self.image = self.h_image
            self.image_rect = self.h_image_rect
        self.h_image_rect.center = self.v_image_rect.center = self.image_rect.center
        self.rotated = not self.rotated

    def check_for_collisions(self, fleet):
        for ship in fleet:
            if ship != self and self.image_rect.colliderect(ship.image_rect):
                return True
        return False

    def default_position(self):
        if self.rotated:
            self.rotate_ship()
        self.image_rect.topleft = self.top_left
        self.h_image_rect.center = self.v_image_rect.center = self.image_rect.center

    def snap_to_grid_edge(self, grid_coords, cell_size):
        if self.image_rect.topleft != self.top_left:

            if self.image_rect.left > grid_coords[0][-1][0] + cell_size or \
                    self.image_rect.right < grid_coords[0][0][0] or \
                    self.image_rect.top > grid_coords[-1][0][1] + cell_size or \
                    self.image_rect.bottom < grid_coords[0][0][1]:
                self.default_position()

            elif self.image_rect.right > grid_coords[0][-1][0] + cell_size:
                self.image_rect.right = grid_coords[0][-1][0] + cell_size
            elif self.image_rect.left < grid_coords[0][0][0]:
                self.image_rect.left = grid_coords[0][0][0]
            elif self.image_rect.top < grid_coords[0][0][1]:
                self.image_rect.top = grid_coords[0][0][1]
            elif self.image_rect.bottom > grid_coords[-1][0][1] + cell_size:
                self.image_rect.bottom = grid_coords[-1][0][1] + cell_size
            self.v_image_rect.center = self.h_image_rect.center = self.image_rect.center

    def snap_to_grid(self, grid_coords, cell_size):
        for row in grid_coords:
            for cell in row:
                if cell[0] <= self.image_rect.left < cell[0] + cell_size \
                        and cell[1] <= self.image_rect.top < cell[1] + cell_size:
                    if self.rotated:
                        self.image_rect.topleft = (cell[0], cell[1] + (cell_size - self.image.get_height()) // 2)
                    else:
                        self.image_rect.topleft = (cell[0] + (cell_size - self.image.get_width()) // 2, cell[1])


        self.h_image_rect.center = self.v_image_rect.center = self.image_rect.center
    
    def __str__(self):
        return 'S'

    # def __int__(self):
    #     return 1