import pygame as pg
from grid import Grid
from wrapper import Wrapper
WIN_SIZE = (1280, 720)
GRID_SIZE = (550, 550)
TOP_LEFT_GRID_LEFT = ((WIN_SIZE[0]//2-GRID_SIZE[0])//2, (WIN_SIZE[1]-GRID_SIZE[1])//4) # top left coord of left grid (ocean)
TOP_LEFT_GRID_RIGHT = (TOP_LEFT_GRID_LEFT[0]+WIN_SIZE[0]//2, TOP_LEFT_GRID_LEFT[1]) # top left coord of right grid   (radar)
GRID_ROW_CNT = 11 # number of rows  (with coord marker)
GRID_COL_CNT = 11 # number of columns (with coord marker)
CELL_SIZE = (GRID_SIZE[0]//GRID_COL_CNT, GRID_SIZE[1]//GRID_ROW_CNT) # size of 1 cell

class Game(Wrapper):
    def __init__(self):
        super().__init__()
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption("Battleships game")
        self.get_images()

        self.left_grid = Grid(TOP_LEFT_GRID_LEFT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)
        self.right_grid = Grid(TOP_LEFT_GRID_RIGHT, GRID_ROW_CNT, GRID_COL_CNT, CELL_SIZE)

        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONUP:
                    print(pg.mouse.get_pos())

    def get_images(self):
        self.ocean_image = self.load_image("assets/grids/ocean_grid.png")
        self.radar_image = self.load_image("assets/grids/radar_grid.png")

        self.screen.blit(self.ocean_image, TOP_LEFT_GRID_LEFT)
        self.screen.blit(self.radar_image, TOP_LEFT_GRID_RIGHT)
        pg.display.update()
    
    def load_image(self, path, rotate=False): # we dont need to pass size here because its already declared as constant
        return super().load_image(path, GRID_SIZE, rotate)