from game import *
from serverdata import ServerData

class OnlineGame(Game):
    def __init__(self, screen):
        self.network = Network()
        self.game_won = False
        self.player = Player()
        self.player.make_shots()
        self.serverdata = ServerData()
        super().__init__(screen)


    
    def start_game(self):
        self.game_started = True
    
    def check_valid_shot(self, board, shot): # we only check if we have not yet shot on given position
        if 0 <= shot[0] <= 9 and 0 <= shot[1] <= 9:
            if board[shot[0]][shot[1]] == 0:
                return True
        return False
    
    def shoot(self, board, shot, grid_coords):
        # TODO add tokens instead of pg rect
        self.shot_sound.play()
        if self.serverdata.get_hit():
            self.hit_sound.play()
            board[shot[0]][shot[1]] = 'X'
        else:
            self.miss_sound.play()
            board[shot[0]][shot[1]] = 'W'
    
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


    