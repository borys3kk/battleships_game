import socket
import pickle
from constants import HOST, PORT
class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = HOST
        self.port = PORT
        self.addr = (self.server, self.port)

    
    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass
    
    def send(self, data):
        try:
            data_to_send = pickle.dumps(data)
            self.client.sendall(data_to_send)
        except socket.error as e:
            print (str(e))
    
    def receive(self):
        try:
            data_from_server = self.client.recv(2048 * 2)
            if not data_from_server:
                return None  # if none is returned, the player wins by forfeit (or the server crashed)
            return pickle.loads(data_from_server)
        except:
            print("somethings not quite right")


