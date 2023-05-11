from ship import Ship
import pygame as pg
import random
from time import sleep
from constants import *



class Computer:
    def __init__(self):
        self.fleet = self.create_fleet()
        self.possible_choices_computer = [(i, j) for i in range(10) for j in range(10)]
        random.shuffle(self.possible_choices_computer)
        self.board = []


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

    def make_attack(self, game):
        sleep(random.randint(10, 15) // 10)  # so its more 'human'
        shot = self.possible_choices_computer.pop()
        game.shoot(game.player.board, shot, game.left_grid.grid_cells_coords)
        game.change_turn()

    def randomize_ships(self, fleet, grid):
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
