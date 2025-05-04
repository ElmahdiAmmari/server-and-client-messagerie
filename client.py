import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("\n" + msg)
        except:
            print("[!] Connection closed.")
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

# Receiving prompt for username
print(client.recv(1024).decode())
username = input()
client.send(username.encode())

# Start thread to receive messages
threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

# Send messages
while True:
    msg = input("To send (format TO:username:message): ")
    if msg.lower() == "quit":
        break
    client.send(msg.encode())
