class ServerData:
    def __init__(self, shot = None, board = None, game_won = False):
        self._shot = shot
        self._board = board
        self._game_won = game_won

    def set_board(self, new_board):
        self._board = new_board
    
    def set_shot(self, new_shot):
        self._shot = new_shot
    
    def set_game_won(self, game_won):
        self._game_won = game_won

    def get_game_won(self):
        return self._game_won
    
    def update_board(self, shot):
        i, j = shot
        if self._board[i][j] == 'S':
            self._board[i][j] = 'X'
        elif self._board[i][j] == 'W':
            self._board[i][j] = 'O'