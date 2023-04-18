from ship import Ship
import pygame as pg
import random
from constants import *

n = GRID_COL_CNT-1

class Player:
    def __init__(self):
        # self.fleet = self.create_fleet()
        self.lost = False
        self.won = False
        self.board = []
        self.ready = False
        self.last_shot = None
        self.player_name = 2
        self.board_to_send = [[0 for _ in range(n)] for _ in range(n)]
        
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

    def update_board(self):
        for i in range(n):
            for j in range(n):
                self.board_to_send[i][j] = str(self.board[i][j])
        print(self.board_to_send)

    def make_attack(self, shot, game):
        game.shoot(game.opponent_board, shot, game.right_grid.grid_cells_coords)
        game.change_turn()
        game.print_board(game.opponent_board)

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
