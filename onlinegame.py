from game import *
from serverdata import ServerData
from datetime import datetime
import time
from os import getpid


class OnlineGame(Game):
    def __init__(self, screen, port):
        self.network = Network(port)
        self.game_won = False

        self.player = Player()

        self.pid = getpid()

        self.data_to_send = ServerData()
        self.callback = None
        self.other_player_connected = False

        self.once = True

        self.callback_thread = None
        self.thread = None
        self.font = pg.font.SysFont("comicsans", 40)

        # TODO ADD CONNECTION STATUS IN GAME
        # self.empty_string = "                                               "
        self.wait_text = "Waiting for your opponent"
        # self.text_rect = self.display_text.get_rect()

        self.network.connect()
        self.cnt = 0
        self.turn = None
        self.your_turn = "                 Your turn!                   "
        self.computer_turn = "Opponent's turn!"

        self.display_text = self.font.render(self.your_turn, True, (255, 255, 255))
        self.text_rect = self.display_text.get_rect()
        self.text_rect.center = (TEXT_POSITION[0], TEXT_POSITION[1])
        super().__init__(screen)

    def get_ready(self):
        print(f"Player with pid: {self.pid}")
        # Starting thread to wait for other player
        self.thread = Thread(target=self.wait_for_other_player)
        self.thread.start()
        while self.running:
            self.clock.tick(60)
            for event in pg.event.get():
                if not self.other_player_connected and self.cnt == 0:
                    print("waiting")
                    self.cnt += 1
                elif self.other_player_connected and (self.cnt == 1 or self.cnt == 0):
                    self.cnt += 2
                    self.thread.join()
                    print("can start game :)")
                    print("Current Time = ", datetime.now().strftime("%H:%M:%S"))
                else:
                    if event.type == pg.QUIT:
                        self.running = False
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if not self.game_started:
                            for ship in self.player.fleet:
                                if ship.v_image_rect.collidepoint(pg.mouse.get_pos()):
                                    ship.active = True
                                    ship.drag_ship(self)
                                    self.update_screen()
                        if self.start_button.click(pg.mouse.get_pos()):
                            if self.all_placed():
                                self.player.board = self.create_game_logic(self.player.fleet,
                                                                           self.left_grid.grid_cells_coords)
                                self.player.make_shots()
                                self.network.send(True)
                                print("YOU START: ", self.turn)
                                self.start_game_on_server()
                            else:
                                sg.Popup("Not all ships have been placed, press r to place them randomly!",
                                         title="Error")
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_r and not self.game_started:
                            self.player.randomize_ships(self.player.fleet, self.left_grid.grid_cells_coords)
                            self.update_screen()

    def wait_for_other_player(self):
        self.other_player_connected = self.network.receive()

    def start_wait_for_ready_thread(self):
        self.thread = Thread(target=self.wait_for_ready)
        self.thread.start()

    def wait_for_ready(self):
        self.turn = self.network.receive()

    def start_game_on_server(self):
        self.start_wait_for_ready_thread()
        self.update_screen()
        self.game_started = True

        if self.turn is None:
            while True:
                self.clock.tick(60)
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.update_round_text()
                        sg.popup("Wait fot other player to get ready!")
                if self.turn is not None:
                    break
        print("GAME STARTED")
        self.update_screen()
        self.update_round_text()
        while self.game_started:
            self.clock.tick(60)
            for event in pg.event.get():
                if self.callback:
                    if self.turn:
                        self.handle_player_turn()
                    else:
                        self.handle_opponent_turn()
                    self.turn = not self.turn
                    self.update_round_text()

                if event.type == pg.QUIT:
                    self.running = False
                    self.game_started = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.turn:
                        shot = self.get_grid_coords(self.right_grid, pg.mouse.get_pos())
                        if self.check_valid_shot(self.player.shots, shot):
                            self.attack(shot)
                if not self.turn and self.once:
                    self.once = not self.once
                    self.start_wait_for_attack_thread()

    def handle_game_finished(self):
        ended = False
        if self.game_won:
            ended = sg.Popup(f"YOU WON! {self.pid}", title="WIN!", keep_on_top=True)
        else:
            ended = sg.Popup(f"OTHER PLAYER WON :/ {self.pid}", title="LOSS!", keep_on_top=True)
        if ended:
            self.callback = None
            self.game_started = False
            self.running = False

    def handle_player_turn(self):
        self.shoot_opponent(self.player.shots, self.callback.get_shot(), self.right_grid.grid_cells_coords)
        self.callback_thread.join()
        if self.callback.get_game_finished():
            self.game_won = self.callback.get_game_won()
            self.handle_game_finished()
        self.callback = None

    def handle_opponent_turn(self):
        self.shoot_player(self.player.board, self.callback.get_shot(), self.left_grid.grid_cells_coords)
        self.thread.join()

        self.game_won = not self.all_destroyed(self.player.fleet)

        self.callback.set_game_finished(not self.game_won)

        if self.callback.get_game_finished():
            self.callback.set_game_won(not self.game_won)
            self.network.send(self.callback)
            self.handle_game_finished()

        self.network.send(self.callback)
        self.callback = None
        self.once = not self.once

    def start_wait_for_attack_thread(self):
        print(f"waiting for attack started with pid: {getpid()}")
        self.thread = Thread(target=self.wait_for_attack)
        self.thread.start()

    def wait_for_attack(self):
        time.sleep(1)
        self.callback = self.network.receive()

    def wait_for_callback(self):
        time.sleep(1)
        self.callback = self.network.receive()

    def start_callback_thread(self):
        self.callback_thread = Thread(target=self.wait_for_callback)
        self.callback_thread.start()

    def attack(self, shot):
        self.send_attack(shot)  # send shot through server
        self.start_callback_thread()  # get callback from server

    def send_attack(self, shot):
        # set the field in array so that we cant shot twice in the same spot
        # prepare data to send
        # send prepared data
        self.player.shots[shot[0]][shot[1]] = 1
        self.data_to_send.set_shot(shot)
        self.data_to_send.set_game_won(None)
        self.data_to_send.set_hit(None)
        self.network.send(self.data_to_send)

    def check_valid_shot(self, board, shot):  # we only check if we have not yet shot on given position
        if 0 <= shot[0] <= 9 and 0 <= shot[1] <= 9:
            if board[shot[0]][shot[1]] == 0:
                return True
            return False

    def shoot_opponent(self, board, shot, grid_coords):
        self.shot_sound.play()
        x, y = grid_coords[shot[0] + 1][shot[1] + 1]

        if self.callback.get_hit():
            self.hit_sound.play()
            board[shot[0]][shot[1]] = 'X'
            self.red_token_rect.topleft = (x, y)
            self.screen.blit(self.red_token, self.red_token_rect)
        else:
            self.miss_sound.play()
            board[shot[0]][shot[1]] = 'W'
            self.blue_token_rect.topleft = (x, y)
            self.screen.blit(self.blue_token, self.blue_token_rect)
        pg.display.update()

    def shoot_player(self, board, shot, grid_coords):
        self.shot_sound.play()
        x, y = grid_coords[shot[0] + 1][shot[1] + 1]
        if board[shot[0]][shot[1]] == 0:
            board[shot[0]][shot[1]] = 2
            self.blue_token_rect.topleft = (x, y)
            self.screen.blit(self.blue_token, self.blue_token_rect)
            self.miss_sound.play()
            self.callback.set_hit(False)
        elif isinstance(board[shot[0]][shot[1]], Ship):
            board[shot[0]][shot[1]].handle_shot()
            board[shot[0]][shot[1]] = 3
            self.red_token_rect.topleft = (x, y)
            self.screen.blit(self.red_token, self.red_token_rect)
            self.hit_sound.play()
            self.callback.set_hit(True)
        pg.display.update()

    def update_round_text(self):
        self.screen.fill(pg.Color("black"), self.text_rect)
        if self.other_player_connected:
            self.display_text = self.font.render(self.your_turn if self.turn else self.computer_turn, True, (255, 255, 255))
        else:
            self.display_text = self.font.render(self.wait_text, True,(255, 255, 255))
        self.text_rect = self.display_text.get_rect()
        self.text_rect.center = (TEXT_POSITION[0], TEXT_POSITION[1])
        self.screen.blit(self.display_text, self.text_rect)
        pg.display.update(self.text_rect)
