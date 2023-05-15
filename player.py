from ship import Ship
import pygame as pg
import random
from constants import *

n = GRID_COL_CNT-1

class Player:
    def __init__(self):
        self.fleet = self.create_fleet()
        self.lost = False
        self.won = False
        self.board = []
        self.ready = False
        self.shots = []

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
    def make_shots(self):
        self.shots = [[0 for i in range(len(self.board))] for j in range(len(self.board))]
        

    def convert_board(self):
        return [[str(self.board[j][i]) if isinstance(self.board[j][i], Ship) else 'W' for i in range(len(self.board))] for j in range(len(self.board))]

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
