WIN_SIZE = (1280, 720)
GRID_SIZE = (550, 550)
TOP_LEFT_GRID_LEFT = (
    (WIN_SIZE[0] // 2 - GRID_SIZE[0]) // 2, (WIN_SIZE[1] - GRID_SIZE[1]) // 4)  # top left coord of left grid (ocean)
TOP_LEFT_GRID_RIGHT = (
    TOP_LEFT_GRID_LEFT[0] + WIN_SIZE[0] // 2, TOP_LEFT_GRID_LEFT[1])  # top left coord of right grid   (radar)
GRID_ROW_CNT = 11  # number of rows  (with coord marker)
GRID_COL_CNT = 11  # number of columns (with coord marker)
CELL_SIZE = (GRID_SIZE[0] // GRID_COL_CNT, GRID_SIZE[1] // GRID_ROW_CNT)  # size of 1 cell
# FLEET = {
#     'battleship': ['battleship', 'assets/ships/battleship/battleship.png', (125, 600), (40, 195), 4],
#     'cruiser': ['cruiser', 'assets/ships/cruiser/cruiser.png', (200, 600), (40, 195), 4],
#     'destroyer': ['destroyer', 'assets/ships/destroyer/destroyer.png', (275, 600), (30, 145), 3],
#     'patrol boat': ['patrol boat', 'assets/ships/patrol boat/patrol boat.png', (425, 600), (20, 95), 2],
#     'submarine': ['submarine', 'assets/ships/submarine/submarine.png', (350, 600), (30, 145), 3],
#     'carrier': ['carrier', 'assets/ships/carrier/carrier.png', (50, 600), (45, 245), 5],
#     'rescue ship': ['rescue ship', 'assets/ships/rescue ship/rescue ship.png', (500, 600), (20, 95), 2]
# }
FLEET = {
    'battleship': ['battleship', 'assets/ships/battleship/battleship.png', (125, 600), (40, 195), 4],
    'cruiser': ['cruiser', 'assets/ships/cruiser/cruiser.png', (200, 600), (40, 195), 4]

}
