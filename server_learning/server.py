from classfile import TestClass
import socket
import pickle

HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)

print("-----------------SERVER STARTED-----------------")

conn1, addr1 = s.accept()
print (f"connected by: {addr1}")

conn2, addr2 = s.accept()
print (f"connected by: {addr2}")

while True:

    data = conn1.recv(2048)

    if not data:
        conn1.close()
        conn2.close()
        break
    
    conn2.send(data)
    data_var = pickle.loads(data)

    data1 = conn2.recv(2048)

    if not data1:
        conn1.close()
        conn2.close()
        break

    conn1.send(data1)
    data_var1 = pickle.loads(data1)


print("-----------------SERVER STOPPED-----------------")