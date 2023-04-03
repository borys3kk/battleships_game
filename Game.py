import pygame as pg
from grid import Grid
from ship import Ship
from wrapper import Wrapper
import random


WIN_SIZE = (1280, 720)
GRID_SIZE = (550, 550)
TOP_LEFT_GRID_LEFT = (
    (WIN_SIZE[0] // 2 - GRID_SIZE[0]) // 2, (WIN_SIZE[1] - GRID_SIZE[1]) // 4)  # top left coord of left grid (ocean)
TOP_LEFT_GRID_RIGHT = (
    TOP_LEFT_GRID_LEFT[0] + WIN_SIZE[0] // 2, TOP_LEFT_GRID_LEFT[1])  # top left coord of right grid   (radar)
GRID_ROW_CNT = 11  # number of rows  (with coord marker)
GRID_COL_CNT = 11  # number of columns (with coord marker)
CELL_SIZE = (GRID_SIZE[0] // GRID_COL_CNT, GRID_SIZE[1] // GRID_ROW_CNT)  # size of 1 cell
FLEET = {
    'battleship': ['battleship', 'assets/ships/battleship/battleship.png', (125, 600), (40, 195)],
    'cruiser': ['cruiser', 'assets/ships/cruiser/cruiser.png', (200, 600), (40, 195)],
    'destroyer': ['destroyer', 'assets/ships/destroyer/destroyer.png', (275, 600), (30, 145)],
    'patrol boat': ['patrol boat', 'assets/ships/patrol boat/patrol boat.png', (425, 600), (20, 95)],
    'submarine': ['submarine', 'assets/ships/submarine/submarine.png', (350, 600), (30, 145)],
    'carrier': ['carrier', 'assets/ships/carrier/carrier.png', (50, 600), (45, 245)],
    'rescue ship': ['rescue ship', 'assets/ships/rescue ship/rescue ship.png', (500, 600), (20, 95)]
}


class Game(Wrapper):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        pg.display.set_caption("Battleships game")
        self.get_images()

        self.left_grid = Grid(TOP_LEFT_GRID_LEFT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)
        self.right_grid = Grid(TOP_LEFT_GRID_RIGHT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)
        self.fleet = self.create_fleet()
        self.draw_fleet()
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for ship in self.fleet:
                        if ship.v_image_rect.collidepoint(pg.mouse.get_pos()):
                            ship.active = True
                            ship.drag_ship(self)
                            self.create_game_logic(self.fleet, self.left_grid.grid_cells_coords)
                            pg.display.update()
                elif event.type == pg.KEYDOWN:
                    self.randomize_ships(self.fleet, self.left_grid.grid_cells_coords)
                    self.create_game_logic(self.fleet, self.left_grid.grid_cells_coords)
                    self.update_screen()

    def get_images(self):
        self.ocean_image = self.load_image("assets/grids/ocean_grid.png")
        self.radar_image = self.load_image("assets/grids/radar_grid.png")
        self.screen.fill((0,0,0))
        self.screen.blit(self.ocean_image, TOP_LEFT_GRID_LEFT)
        self.screen.blit(self.radar_image, TOP_LEFT_GRID_RIGHT)
        pg.display.update()


    def load_image(self, path, rotate=False):  # we dont need to pass size here because its already declared as constant
        return super().load_image(path, GRID_SIZE, rotate)

    def create_fleet(self):
        fleet = []
        for name in FLEET.keys():
            fleet.append(Ship(name,
                              FLEET[name][1],
                              FLEET[name][2],
                              FLEET[name][3]
                              ))

        return fleet

    def draw_fleet(self):
        for ship in self.fleet:
            ship.draw(self.screen)
            ship.snap_to_grid_edge(self.left_grid.grid_cells_coords, CELL_SIZE[0])
            ship.snap_to_grid(self.left_grid.grid_cells_coords, CELL_SIZE[0])
        pg.display.update()

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        self.get_images()
        self.draw_fleet()
        pg.display.update()

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
                ship.snap_to_grid_edge(self.left_grid.grid_cells_coords,CELL_SIZE[0])
                ship.snap_to_grid(self.left_grid.grid_cells_coords,CELL_SIZE[0])
                if placed_ships:
                    for item in placed_ships:
                        if ship.image_rect.colliderect(item.image_rect):
                            valid_position = False
                            break
                        else:
                            valid_position = True
                else: valid_position = True
            placed_ships.append(ship)

    def create_game_logic(self,fleet,grid_coords):
        n = GRID_COL_CNT-1
        game_logic = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for ship in fleet:
                    if pg.rect.Rect(grid_coords[i+1][j+1][0],grid_coords[i+1][j+1][1],CELL_SIZE[0],CELL_SIZE[1]).colliderect(ship.image_rect):
                        game_logic[i][j] = 1
        for row in game_logic:
            print(row)
        print()
        return game_logic




