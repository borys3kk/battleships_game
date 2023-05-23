from classfile import TestClass
import socket
import pickle

HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
board = [[(j, i) for i in range(10)] for j in range(10)]
var = TestClass(board)

data_to_send = pickle.dumps(var)
s.send(data_to_send)

while True:
    try:
        var.empty_data_to_send = input("Pass what do you want to send: ")
        data_to_send = pickle.dumps(var)
        s.send(data_to_send)
    except KeyboardInterrupt:
        print("Okay bye!")
        break
    data_from_server = s.recv(2048)

    if not data_from_server:
        break
    to_print = pickle.loads(data_from_server)
    print(to_print.start_board)

s.close()
print("data should have been sent")