from constants import HOST, PORTS
from serverroom import ServerRoom
from threading import Thread
class Server():
    def __init__(self):
        print("-----------------SERVER STARTED-----------------")

        self.num_of_rooms = 5
        self.rooms = []
        for i in range(self.num_of_rooms):
            self.rooms.append(ServerRoom(HOST, PORTS[i]))

        self.threads = [None for i in range(self.num_of_rooms)]

    def start_rooms(self):
        for i in range(self.num_of_rooms):
            self.threads[i] = Thread(target=self.rooms[i].handle_players)
            self.threads[i].start()
            print("thread started")

    def join_threads(self):
        for thread in self.threads:
            thread.join()
        
        print("-----------------SERVER STOPPED-----------------")
    

if __name__ == "__main__":
    server = Server()
    try:
        server.start_rooms()
    except KeyboardInterrupt:
        server.join_threads()
