import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

client.send("hello from client".encode())
print(client.recv(1024).decode())