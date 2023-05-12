from random import choice
import socket
import pickle
from constants import HOST, PORT
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
print("-----------------SERVER STARTED-----------------")

whose_turn = choice([True, False])
print(whose_turn)

conn1, addr1 = s.accept()
print(f"connected by: {addr1}")
# while True:
#     conn1.send(pickle.dumps("wait"))
#     print("xdd")
#     conn2, addr2 = s.accept()
#     if conn2:
#         print(f"connected by: {addr2}")
#         conn1.send(pickle.dumps("okay"))
#         conn2.send(pickle.dumps("okay"))
#         break


# time.sleep(1)
# conn2.send(pickle.dumps(not whose_turn))
# conn1.send(pickle.dumps(whose_turn))
while True:
    data = conn1.recv(2048 * 8)
    # data1 = conn2.recv(2048 * 16)
    data1 = True
    if not data or not data1:
        conn1.close()
        # conn2.close()
        break
    print(pickle.loads(data))
    # print(pickle.loads(data1))
    # conn1.send(data1)
    # conn2.send(data)


print("-----------------SERVER STOPPED-----------------")