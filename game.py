import pygame as pg
from grid import Grid
from ship import Ship
from computer import Computer
from wrapper import Wrapper
from network import Network
from numpy import abs
from random import randint, shuffle
from time import sleep
from player import Player
from constants import *
from button import Button
import socket
import PySimpleGUI as sg

# player opponent board values
# 0 - water -> 2
# S - ship -> 3
# 2 - missed in water -> None
# 3 - ship - hit -> None

class Game(Wrapper):
    def __init__(self, screen, type):
        super().__init__()
        self.screen = screen
        pg.display.set_caption("Battleships game")
        self.network = Network()

        # Images 
        self.load_images()
        self.left_grid = Grid(TOP_LEFT_GRID_LEFT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)
        self.right_grid = Grid(TOP_LEFT_GRID_RIGHT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)

        self.player_turn = 1

        # Create players
        self.player = Player()

        if type == 'computer':
            self.opponent = Computer()
            self.opponent_fleet = self.opponent.create_fleet()
            self.opponent_board = []
        else:
            self.network.connect()
            # while self.network.receive() != "okay":
            #     print("waiting")
            self.network.send(self.player)
            return
            # self.opponent = self.network.receive()
            # self.player_turn = self.network.receive()
            # print(self.player_turn)

        # Sounds
        self.shot_sound = pg.mixer.Sound("assets/sounds/gunshot.wav")
        self.hit_sound = pg.mixer.Sound("assets/sounds/explosion.wav")
        self.miss_sound = pg.mixer.Sound("assets/sounds/splash.wav")


        self.running = True
        self.game_started = False

        self.start_button = Button("Start", TOP_LEFT_GRID_RIGHT[0], TOP_LEFT_GRID_RIGHT[1] + GRID_SIZE[1] + 20,
                                   (255, 255, 255), 200,100)

        # self.player_board = []

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
                            if type == "computer":
                                self.start_game()
                            else:
                                self.start_game_on_server()
                        else:
                            sg.Popup("Not all ships have been places, press r to place them randomly!", title="Error")
                    else:
                        self.get_grid_coords(self.right_grid, pg.mouse.get_pos())
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r and not self.game_started:
                        self.player.randomize_ships(self.player.fleet, self.left_grid.grid_cells_coords)
                        self.update_screen()


    def start_game_on_server(self):
        n = GRID_COL_CNT - 1
        self.opponent.board = [[0 for _ in range(n)] for _ in range(n)]
        self.game_started = True
        self.opponent.board = self.network.receive()
        self.opponent.update_board()
        while self.game_started:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.game_started = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.player_turn:
                        shot = self.get_grid_coords(self.right_grid, pg.mouse.get_pos())
                        if self.check_valid_shot(self.opponent.board, shot):
                            self.player.make_attack(shot)


    def start_game(self):
        self.game_started = True
        self.update_screen()
        self.opponent.randomize_ships(self.opponent_fleet, self.right_grid.grid_cells_coords)
        self.opponent.opponent_board = self.create_game_logic(self.opponent_fleet, self.right_grid.grid_cells_coords)
        while self.game_started:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.game_started = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.player_turn:
                        shot = self.get_grid_coords(self.right_grid, pg.mouse.get_pos())
                        if self.check_valid_shot(self.opponent_board, shot):
                            self.player.make_attack()

                            if self.all_destroyed(self.opponent_fleet):
                                self.game_started = False
                                sg.Popup("YOU WON!", title="WIN!")
                                break
                if not self.player_turn:
                    self.opponent.make_attack()

                    if self.all_destroyed(self.player.fleet):
                        self.game_started = False
                        sg.Popup("COMPUTER WON :/", title="LOSS!")

    def check_valid_shot(self, board, shot):
        if 0 <= shot[0] <= 9 and 0 <= shot[1] <= 9:
            if board[shot[0]][shot[1]] == 0 or isinstance(board[shot[0]][shot[1]], Ship):
                return True
        return False

    def print_board(self, board):
        for row in board:
            for c in row:
                print(str(c), end=' ')
            print()

    def shoot(self, board, shot, grid_coords):
        self.shot_sound.play()
        x, y = grid_coords[shot[0] + 1][shot[1] + 1]
        if board[shot[0]][shot[1]] == 0:
            board[shot[0]][shot[1]] = 2
            pg.draw.rect(self.screen, (255, 0, 0), pg.Rect(x, y, 50, 50))
            self.miss_sound.play()
        elif isinstance(board[shot[0]][shot[1]], Ship):
            board[shot[0]][shot[1]].handle_shot()
            board[shot[0]][shot[1]] = 3
            pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(x, y, 50, 50))
            self.hit_sound.play()
        pg.display.update()

    def change_turn(self):
        self.turn = (self.turn + 1) % 2

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

    def draw_fleet(self):
        for ship in self.player.fleet:
            ship.draw(self.screen)
        # pg.display.update()

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_fleet()
        if not self.game_started:
            self.draw_button()
        pg.display.update()

    # def randomize_ships(self,fleet,grid):
    #     placed_ships = []
    #     for ship in fleet:
    #         valid_position = False
    #         while not valid_position:
    #             ship.default_position()
    #             rotate = random.choice([True,False])
    #             if rotate:
    #                 y = random.randint(1, 10)
    #                 x = random.randint(1,10-(ship.h_image.get_width()//CELL_SIZE[1]))
    #                 ship.rotate_ship()
    #             else:
    #                 y = random.randint(1,10-(ship.h_image.get_height()//CELL_SIZE[0]))
    #                 x = random.randint(1,10)
    #             ship.image_rect.topleft = grid[y][x]
    #             ship.snap_to_grid_edge(grid,CELL_SIZE[0])
    #             ship.snap_to_grid(grid,CELL_SIZE[0])
    #             if placed_ships:
    #                 for item in placed_ships:
    #                     if ship.image_rect.colliderect(item.image_rect):
    #                         valid_position = False
    #                         break
    #                     else:
    #                         valid_position = True
    #             else: valid_position = True
    #         ship.placed = True
    #         placed_ships.append(ship)

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
