WIN_SIZE = (1280, 960)
GRID_SIZE = (550, 550)
TOP_LEFT_GRID_LEFT = (
    (WIN_SIZE[0] // 2 - GRID_SIZE[0]) // 2, (WIN_SIZE[1] - GRID_SIZE[1]) // 4)  # top left coord of left grid (ocean)
TOP_LEFT_GRID_RIGHT = (
    TOP_LEFT_GRID_LEFT[0] + WIN_SIZE[0] // 2, TOP_LEFT_GRID_LEFT[1])  # top left coord of right grid   (radar)
GRID_ROW_CNT = 11  # number of rows  (with coord marker)
GRID_COL_CNT = 11  # number of columns (with coord marker)
CELL_SIZE = (GRID_SIZE[0] // GRID_COL_CNT, GRID_SIZE[1] // GRID_ROW_CNT)  # size of 1 cell
HOST = '127.0.0.1'
PORT = 65432
MENU_IMAGE_PATH = 'assets/backgrounds/Battleship.jpg'
START_SHIP_Y = TOP_LEFT_GRID_LEFT[1] + GRID_SIZE[1] + 20
TEXT_POSITION = (WIN_SIZE[0]//2, 20)
BUTTON_POSITION = (TOP_LEFT_GRID_RIGHT[0], TOP_LEFT_GRID_RIGHT[1] + GRID_SIZE[1] + 20)
HELP_POSITION = (TOP_LEFT_GRID_RIGHT[0] + CELL_SIZE[0] * 5, BUTTON_POSITION[1])
FLEET = {
    'battleship': ['battleship', 'assets/ships/battleship/battleship.png', (125,START_SHIP_Y ), (40, 195), 4],
    'cruiser': ['cruiser', 'assets/ships/cruiser/cruiser.png', (200, START_SHIP_Y), (40, 195), 4],
    'destroyer': ['destroyer', 'assets/ships/destroyer/destroyer.png', (275, START_SHIP_Y), (30, 145), 3],
    'patrol_boat': ['patrol_boat', 'assets/ships/patrol boat/patrol boat.png', (425, START_SHIP_Y), (20, 95), 2],
    'submarine': ['submarine', 'assets/ships/submarine/submarine.png', (350, START_SHIP_Y), (30, 145), 3],
    'carrier': ['carrier', 'assets/ships/carrier/carrier.png', (50, START_SHIP_Y), (45, 245), 5],
    'rescue_ship': ['rescue_ship', 'assets/ships/rescue ship/rescue ship.png', (500, START_SHIP_Y), (20, 95), 2]
}

DIRECTIONS = [(1,0),(-1,0),(0,1),(0,-1)]
# FLEET = {
#     'battleship': ['battleship', 'assets/ships/battleship/battleship.png', (125, 600), (40, 195), 4],
#     'cruiser': ['cruiser', 'assets/ships/cruiser/cruiser.png', (200, 600), (40, 195), 4]

# }
