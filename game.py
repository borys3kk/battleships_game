import pygame as pg
from grid import Grid
from ship import Ship
from computer import Computer
from wrapper import Wrapper
from network import Network
from numpy import abs
from random import randint, shuffle, choice
from time import sleep
from player import Player
from constants import *
from button import Button
import socket
import PySimpleGUI as sg
from threading import Thread # will use it later
# player opponent board values
# 0 - water -> 2
# S - ship -> 3
# 2 - missed in water -> None
# 3 - ship - hit -> None

class Game(Wrapper):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        pg.display.set_caption("Battleships game")

        # Images 
        self.load_images()
        self.left_grid = Grid(TOP_LEFT_GRID_LEFT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)
        self.right_grid = Grid(TOP_LEFT_GRID_RIGHT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)

        # Sounds
        self.shot_sound = pg.mixer.Sound("assets/sounds/gunshot.wav")
        self.hit_sound = pg.mixer.Sound("assets/sounds/explosion.wav")
        self.miss_sound = pg.mixer.Sound("assets/sounds/splash.wav")
        self.red_token = self.load_image('assets/tokens/redtoken.png', CELL_SIZE)
        self.red_token_rect = self.red_token.get_rect()

        self.blue_token = self.load_image('assets/tokens/bluetoken.png', CELL_SIZE)
        self.blue_token_rect = self.blue_token.get_rect()

        self.running = True
        self.game_started = False

        self.start_button = Button("Start", BUTTON_POSITION[0], BUTTON_POSITION[1], (255, 255, 255), 200,100)

        self.help_font = pg.font.SysFont("comicsans", 30)
        
        self.update_screen()
        self.clock = pg.time.Clock()

        while self.running:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not self.game_started:  # when the game has not started yet
                        for ship in self.player.fleet:
                            if ship.v_image_rect.collidepoint(pg.mouse.get_pos()):
                                ship.active = True
                                ship.drag_ship(self)
                                self.update_screen()
                    if self.start_button.click(pg.mouse.get_pos()):
                        if self.all_placed():
                            self.player.board = self.create_game_logic(self.player.fleet,
                                                                       self.left_grid.grid_cells_coords)
                            self.start_game()
                        else:
                            sg.Popup("Not all ships have been placed, press r to place them randomly!", title="Error")
                    else:
                        self.get_grid_coords(self.right_grid, pg.mouse.get_pos())
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r and not self.game_started:
                        self.player.randomize_ships(self.player.fleet, self.left_grid.grid_cells_coords)
                        self.update_screen()

    def check_valid_shot(self, board, shot):
        pass

    def print_board(self, board):
        for row in board:
            for c in row:
                print(str(c), end=' ')
            print()
    
    def make_attack(self, shot):
        pass

    def shoot(self, board, shot, grid_coords):
        pass
    

    def load_images(self):
        self.ocean_image = self.load_image_from_disk("assets/grids/ocean_grid.png")
        self.radar_image = self.load_image_from_disk("assets/grids/radar_grid.png")

    def draw_grid(self):
        self.screen.blit(self.ocean_image, TOP_LEFT_GRID_LEFT)
        self.screen.blit(self.radar_image, TOP_LEFT_GRID_RIGHT)

    def draw_button(self):
        self.start_button.draw(self.screen)

    def all_placed(self):
        for ship in self.player.fleet:
            if not ship.placed:
                return False
        return True

    def all_destroyed(self, fleet):
        for ship in fleet:
            if not ship.destroyed:
                return False
        return True

    def load_image_from_disk(self, path,
                             rotate=False):  # we dont need to pass size here because its already declared as constant
        return super().load_image(path, GRID_SIZE, rotate)

    def draw_fleet(self):
        for ship in self.player.fleet:
            ship.draw(self.screen)
            
    def update_round_text(self):
        pass

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_fleet()
        if not self.game_started:
            self.draw_button()
            self.show_help()
        pg.display.update()

    def show_help(self):
        line_1 = "            HELP"
        line_2 = "1 - rotate current ship"
        line_3 = "r - place ships randomly"
        lines = [line_1, line_2, line_3]
        for idx, line in enumerate(lines):
            text = self.help_font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (HELP_POSITION[0], HELP_POSITION[1] + idx * 30))


    def create_game_logic(self, fleet, grid_coords):
        n = GRID_COL_CNT - 1
        game_logic = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for ship in fleet:
                    if pg.rect.Rect(grid_coords[i + 1][j + 1][0], grid_coords[i + 1][j + 1][1], CELL_SIZE[0],
                                    CELL_SIZE[1]).colliderect(ship.image_rect):
                        game_logic[i][j] = ship
        return game_logic

    def get_grid_coords(self, grid: Grid, mouse_pos):  # get grid coords for shooting (pew pew)
        i = abs(grid.top_left_corner[0] - mouse_pos[0]) // CELL_SIZE[0]
        j = abs(grid.top_left_corner[1] - mouse_pos[1]) // CELL_SIZE[1]
        return j - 1, i - 1
