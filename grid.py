class Grid:
    def __init__(self, top_left_corner, grid_row_cnt, grid_col_cnt, cell_size):
        self.top_left_corner = top_left_corner
        self.grid_row_cnt = grid_row_cnt
        self.grid_col_cnt = grid_col_cnt
        self.cell_size = cell_size
        self.grid_cells_coords = [[[0,0] for i in range(self.grid_col_cnt)] for j in range(self.grid_row_cnt)] # including coords
        self.get_grid_coords()
    
    def get_grid_coords(self): # initializing coords of each cell in our grid
        self.grid_cells_coords[0][0] = [self.top_left_corner[0], self.top_left_corner[1]]
        for i in range(self.grid_row_cnt):
            for j in range(self.grid_col_cnt):
                if i == j == 0:
                    continue
                if j > 0:
                    self.grid_cells_coords[i][j][0] += self.grid_cells_coords[i][j-1][0]
                    self.grid_cells_coords[i][j][0] += self.cell_size[0]
                    self.grid_cells_coords[i][j][1] += self.grid_cells_coords[i][j-1][1]
                else:
                    self.grid_cells_coords[i][j][1] += self.grid_cells_coords[i-1][j][1]
                    self.grid_cells_coords[i][j][1] += self.cell_size[1]
                    self.grid_cells_coords[i][j][0] += self.grid_cells_coords[i-1][j][0]