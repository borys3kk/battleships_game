from ship import Ship
import pygame as pg
import random
from time import sleep
from constants import *



class Computer:
    def __init__(self):
        self.fleet = self.create_fleet()
        self.possible_moves = [(i, j) for i in range(10) for j in range(10)]
        random.shuffle(self.possible_moves)
        self.board = []
        self.moves = []


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

        # shot = self.possible_moves.pop()
        # is_hitted = game.shoot(game.player.board, shot, game.left_grid.grid_cells_coords)
        # game.change_turn()
        print(self.moves)
        if len(self.moves) > 0:
            random.shuffle(self.moves)
            x,y = self.moves.pop()
            is_hit = game.shoot(game.player.board,(x,y),game.left_grid.grid_cells_coords)
            self.possible_moves.remove((x,y))

        else:
            x,y = self.possible_moves.pop()
            is_hit = game.shoot(game.player.board, (x,y), game.left_grid.grid_cells_coords)
        if is_hit:
            self.moves = []

            for direction in DIRECTIONS:
                print((x + direction[0], y + direction[1]))
                if (x + direction[0], y + direction[1]) in self.possible_moves:
                    self.moves.append((x + direction[0], y + direction[1]))
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
