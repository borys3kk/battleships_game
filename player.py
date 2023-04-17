from ship import Ship
import pygame as pg
import random
from constants import *


class Player:
    def __init__(self,game):
        self.fleet = self.create_fleet()
        self.game = game

    def create_fleet(self):
        fleet = []
        for name in FLEET.keys():
            fleet.append(Ship(name,
                              FLEET[name][1],
                              FLEET[name][2],
                              FLEET[name][3],
                              FLEET[name][4]
                              ))

        return fleet

    def make_attack(self):
        shot = self.game.get_grid_coords(self.game.right_grid, pg.mouse.get_pos())
        if self.game.check_valid_shot(self.game.opponent_board, shot):
            self.game.shoot(self.game.opponent_board, shot, self.game.right_grid.grid_cells_coords)
            self.game.change_turn()
            self.game.print_board(self.game.opponent_board)

    def randomize_ships(self,fleet,grid):
        placed_ships = []
        for ship in fleet:
            valid_position = False
            while not valid_position:
                ship.default_position()
                rotate = random.choice([True,False])
                if rotate:
                    y = random.randint(1, 10)
                    x = random.randint(1,10-(ship.h_image.get_width()//CELL_SIZE[1]))
                    ship.rotate_ship()
                else:
                    y = random.randint(1,10-(ship.h_image.get_height()//CELL_SIZE[0]))
                    x = random.randint(1,10)
                ship.image_rect.topleft = grid[y][x]
                ship.snap_to_grid_edge(grid,CELL_SIZE[0])
                ship.snap_to_grid(grid,CELL_SIZE[0])
                if placed_ships:
                    for item in placed_ships:
                        if ship.image_rect.colliderect(item.image_rect):
                            valid_position = False
                            break
                        else:
                            valid_position = True
                else: valid_position = True
            ship.placed = True
            placed_ships.append(ship)
