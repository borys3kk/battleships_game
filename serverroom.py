from random import choice
import socket
import pickle
from threading import Thread
from datetime import datetime

class ServerRoom():
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)

        self.player_1_turn = choice([True, False])
        self.player_2_turn = not self.player_1_turn

        self.player_1_conn = None
        self.player_1_addr = None

        self.player_2_conn = None
        self.player_2_addr = None

        self.player_1_ready = False
        self.player_2_ready = False

        self.player_1_thread = None
        self.player_2_thread = None


    def handle_players(self):
        print("-----------------ROOM STARTED-----------------")
        
        self.listen_for_players()
        self.wait_for_ready()
        self.send_who_starts()
        self.send_data_between_clients()

        print("-----------------ROOM STOPPED-----------------")


    def listen_for_players(self):
        self.player_1_conn, self.player_1_addr = self.server.accept()
        print(f"connected by: {self.player_1_addr}")
        while True:
            self.player_2_conn, self.player_2_addr = self.server.accept()
            if self.player_2_conn:
                print(f"connected by: {self.player_2_addr}")
                self.player_2_conn.send(pickle.dumps(True))
                self.player_1_conn.send(pickle.dumps(True))
                break

    def send_data_between_clients(self):
        while True:
            if self.player_1_turn:
                
                current_time = datetime.now().strftime("%H:%M:%S")
                print("Time before getting data to send in player 1 = ", current_time) 

                data_to_send = self.player_1_conn.recv(1024)
                self.player_2_conn.send(data_to_send)
                callback = self.player_2_conn.recv(1024)
                self.player_1_conn.send(callback)

                current_time = datetime.now().strftime("%H:%M:%S")
                print("Time after sending callback (player two) = ", current_time) 

                self.player_1_turn = not self.player_1_turn
            
            else:
                current_time = datetime.now().strftime("%H:%M:%S")
                print("Time before getting data to send in player 2 = ", current_time) 

                data_to_send = self.player_2_conn.recv(1024)
                self.player_1_conn.send(data_to_send)
                callback = self.player_1_conn.recv(1024)
                self.player_2_conn.send(callback)
                
                current_time = datetime.now().strftime("%H:%M:%S")
                print("Time after sending callback (player one) = ", current_time) 
                
                self.player_1_turn = not self.player_1_turn
            if callback:
                callback_data = pickle.loads(callback)
                if callback_data.get_game_finished():
                    break

    def send_who_starts(self):
        self.player_1_conn.send(pickle.dumps(self.player_1_turn))
        self.player_2_conn.send(pickle.dumps(self.player_2_turn))

    def join_player_threads(self):
        self.player_1_thread.join()
        self.player_2_thread.join()

    def wait_for_ready(self):
        self.player_1_thread = Thread(target=self.get_player_1_ready)
        self.player_1_thread.start()

        self.player_2_thread = Thread(target=self.get_player_2_ready)
        self.player_2_thread.start()

        while True:
            if self.player_1_ready and self.player_2_ready:
                self.join_player_threads()
                break

    def get_player_1_ready(self):
        print("Starting to receive data! (player one)")
        ready = self.player_1_conn.recv(2048 * 2)
        self.player_1_ready =  pickle.loads(ready)

    def get_player_2_ready(self):
        print("Starting to receive data! (player two)")
        ready = self.player_2_conn.recv(2048 * 2)
        self.player_2_ready =  pickle.loads(ready)