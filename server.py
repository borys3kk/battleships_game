import socket
import pickle
from player import Player

HOST = '127.0.0.1'
PORT = 33000
users = 0

# TODO SZYMON ogarnąc serwer
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("-------------SERVER STARTED-------------")
    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        str(e)
    
    s.listen(2)

    client_socket1, address1 = s.accept()
    client_socket2, address2 = s.accept()
    while True:
        print(client_socket1.recv(1024))
        print(address1, address2)

