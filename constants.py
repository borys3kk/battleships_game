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
PORT = 33000
MENU_IMAGE_PATH = 'assets/backgrounds/Battleship.jpg'


FLEET = { # TODO Piotr zrobić automatyczne znajdowanie pozycji pierwotnych statków!
    'battleship': ['battleship', 'assets/ships/battleship/battleship.png', (125, 700), (40, 195), 4],
    'cruiser': ['cruiser', 'assets/ships/cruiser/cruiser.png', (200, 700), (40, 195), 4],
    'destroyer': ['destroyer', 'assets/ships/destroyer/destroyer.png', (275, 700), (30, 145), 3],
    'patrol boat': ['patrol boat', 'assets/ships/patrol boat/patrol boat.png', (425, 700), (20, 95), 2],
    'submarine': ['submarine', 'assets/ships/submarine/submarine.png', (350, 700), (30, 145), 3],
    'carrier': ['carrier', 'assets/ships/carrier/carrier.png', (50, 700), (45, 245), 5],
    'rescue ship': ['rescue ship', 'assets/ships/rescue ship/rescue ship.png', (500, 700), (20, 95), 2]
}
# FLEET = {
#     'battleship': ['battleship', 'assets/ships/battleship/battleship.png', (125, 600), (40, 195), 4],
#     'cruiser': ['cruiser', 'assets/ships/cruiser/cruiser.png', (200, 600), (40, 195), 4]

# }
