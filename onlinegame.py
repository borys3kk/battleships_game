from game import *
from serverdata import ServerData
from datetime import datetime
from time import sleep
from os import getpid
class OnlineGame(Game):
    def __init__(self, screen):
        self.network = Network()
        self.game_won = False

        self.player = Player()
        
        self.network = Network()

        self.data_to_send = ServerData()
        self.callback = None
        self.other_player_connected = False
        
        self.once = True

        self.callback_thread = None
        self.thread = None

        # TODO ADD CONNECTION STATUS IN GAME
        # self.empty_string = "                                               "
        # self.connection_info = self.font.render("Waiting for other player" if not self.other_player_connected else "Other player connected!", True, (255, 255, 255))
        # self.text_rect = self.turn_text.get_rect()

        self.network.connect()
        self.cnt = 0
        self.turn = None
        super().__init__(screen)


    def get_ready(self):
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
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print("Current Time = ", current_time)   
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
                                self.player.board = self.create_game_logic(self.player.fleet, self.left_grid.grid_cells_coords)
                                self.player.make_shots()
                                self.network.send(True)
                                self.turn = self.network.receive()
                                print("YOU START: ", self.turn)
                                self.start_game_on_server()
                            else:
                                sg.Popup("Not all ships have been placed, press r to place them randomly!", title="Error")
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_r and not self.game_started:
                            self.player.randomize_ships(self.player.fleet, self.left_grid.grid_cells_coords)
                            self.update_screen()

    def wait_for_other_player(self):
        self.other_player_connected = self.network.receive()

    def start_game_on_server(self):
        self.game_started = True
        print("GAME STARTED")
        self.update_screen()
        while self.game_started:
            self.clock.tick(60)
            for event in pg.event.get():
                if self.callback:
                    if self.turn:
                        self.shoot(self.player.shots, self.callback.get_shot(), self.right_grid.grid_cells_coords)
                        self.callback = None
                        self.callback_thread.join()
                    else:
                        self.shoot(self.player.board, self.callback.get_shot(), self.left_grid.grid_cells_coords)
                        self.network.send(self.callback)
                        self.callback = None
                        self.thread.join()
                    self.turn = not self.turn

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

    def start_wait_for_attack_thread(self):
        print(f"waiting for attack starte with pid: {getpid()}")
        self.thread = Thread(target=self.wait_for_attack)
        self.thread.start()

    def wait_for_attack(self):
        self.callback = self.network.receive()

    def wait_for_callback(self):
        self.callback = self.network.receive()

    def start_callback_thread(self):
        self.callback_thread = Thread(target=self.wait_for_callback)
        self.callback_thread.start()

    def attack(self, shot):
        self.send_attack(shot) # send shot through server
        self.start_callback_thread() # get callback from server

    def send_attack(self, shot):
        # set the field in array so that we cant shot twice in the same spot
        # prepare data to send
        # send prepared data
        self.player.shots[shot[0]][shot[1]] = 1
        self.data_to_send.set_shot(shot)
        self.data_to_send.set_game_won(False)
        self.data_to_send.set_hit(None)
        self.network.send(self.data_to_send)

    def check_valid_shot(self, board, shot): # we only check if we have not yet shot on given position
        if 0 <= shot[0] <= 9 and 0 <= shot[1] <= 9:
            if board[shot[0]][shot[1]] == 0:
                return True
            return False
    
    def shoot(self, board, shot, grid_coords):
        # TODO add tokens instead of pg rect
        print(shot)
        self.shot_sound.play()
        x, y = grid_coords[shot[0] + 1][shot[1] + 1]
        print(x, y)
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
