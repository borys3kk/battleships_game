from game import *

class LocalGame(Game):
    def __init__(self, screen):
        self.player = Player()
        self.opponent = Computer()
        self.player_turn = choice([True, False])
        super().__init__(screen)
    

    def start_game(self):
        self.game_started = True
        self.update_screen()
        self.opponent.randomize_ships(self.opponent.fleet, self.right_grid.grid_cells_coords)
        self.opponent.board = self.create_game_logic(self.opponent.fleet, self.right_grid.grid_cells_coords)
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
                            self.make_attack(shot)

                            if self.all_destroyed(self.opponent.fleet):
                                self.game_started = False
                                sg.Popup("YOU WON!", title="WIN!", keep_on_top=True)
                                break
                if not self.player_turn:
                    self.opponent.make_attack(self)

                    if self.all_destroyed(self.player.fleet):
                        self.game_started = False
                        sg.Popup("COMPUTER WON :/", title="LOSS!", keep_on_top=True)

    def change_turn(self):
        self.player_turn = not self.player_turn
    
    def check_valid_shot(self, board, shot):
        if 0 <= shot[0] <= 9 and 0 <= shot[1] <= 9:
            if board[shot[0]][shot[1]] == 0 or isinstance(board[shot[0]][shot[1]], Ship):
                return True
        return False

    def make_attack(self, shot):
        self.shoot(self.opponent.board, shot, self.right_grid.grid_cells_coords)
        self.change_turn()
        # game.print_board(game.opponent.board)
    
    def shoot(self, board, shot, grid_coords):
        # TODO add tokens instead of pg rect
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
        