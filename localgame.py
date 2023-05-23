from game import *

class LocalGame(Game):
    def __init__(self, screen):
        self.player = Player()
        self.opponent = Computer()
        self.player_turn = choice([True, False])
        
        self.your_turn =     "                 Your turn!                   "
        self.computer_turn = "Waiting for computer's turn!"

        self.font = pg.font.SysFont("comicsans", 40)
        self.turn_text = self.font.render(self.your_turn if self.player_turn else self.computer_turn, True, (255, 255, 255))
        self.text_rect = self.turn_text.get_rect()
        self.text_rect.center = (TEXT_POSITION[0], TEXT_POSITION[1])

        super().__init__(screen)


    def start_game(self):
        self.game_started = True
        self.update_screen()
        self.update_round_text()
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

    def update_round_text(self):
        self.screen.fill(pg.Color("black"), self.text_rect)
        self.turn_text = self.font.render(self.your_turn if self.player_turn else self.computer_turn, True, (255, 255, 255))
        self.text_rect = self.turn_text.get_rect()
        self.text_rect.center = (TEXT_POSITION[0], TEXT_POSITION[1])
        self.screen.blit(self.turn_text, self.text_rect)
        pg.display.update(self.text_rect)

    def change_turn(self):
        self.player_turn = not self.player_turn
        self.update_round_text()
    
    def check_valid_shot(self, board, shot):
        if 0 <= shot[0] <= 9 and 0 <= shot[1] <= 9:
            if board[shot[0]][shot[1]] == 0 or isinstance(board[shot[0]][shot[1]], Ship):
                return True
        print("not valid")
        return False

    def make_attack(self, shot):
        self.shoot(self.opponent.board, shot, self.right_grid.grid_cells_coords)
        self.change_turn()
    
    def shoot(self, board, shot, grid_coords):
        self.shot_sound.play()
        x, y = grid_coords[shot[0] + 1][shot[1] + 1]
        if board[shot[0]][shot[1]] == 0:
            board[shot[0]][shot[1]] = 2
            self.blue_token_rect.topleft = (x, y)
            self.screen.blit(self.blue_token, self.blue_token_rect)
            self.miss_sound.play()
            pg.display.update()
            return False
        elif isinstance(board[shot[0]][shot[1]], Ship):
            board[shot[0]][shot[1]].handle_shot()
            board[shot[0]][shot[1]] = 3
            self.red_token_rect.topleft = (x, y)
            self.screen.blit(self.red_token, self.red_token_rect)
            self.hit_sound.play()
            pg.display.update()
            return True

        