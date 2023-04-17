import socket

HOST = '127.0.0.1'
PORT = 33000
users = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
client_socket1 = False
client_socket2 = False

while not client_socket1:
    client_socket1, address = s.accept()
    print(address)

while not client_socket2:
    client_socket2, address = s.accept()
    print(address)




