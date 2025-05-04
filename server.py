import socket
import threading

clients = {}  # username -> socket

def handle_client(client_socket):
    username = None
    try:
        # Step 1: Ask for username and stor it in the clients dictionnairy
        client_socket.send("Enter your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        clients[username] = client_socket
        print(f"[+] {username} connected.")

        while True:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break

            # Step 2: Expect format TO:target:message
            if msg.startswith("TO:"):
                try:
                    _, target_user, content = msg.split(":", 2)
                    if target_user in clients:
                        clients[target_user].send(f"{username}: {content}".encode())
                    else:
                        client_socket.send(f"[Server] User {target_user} not found.".encode())
                except ValueError:
                    client_socket.send(b"[Server] Invalid message format. Use TO:username:message")
            else:
                client_socket.send(b"[Server] Use format TO:username:message")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()
        if username in clients:
            del clients[username]
        print(f"[-] {username} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(10)
    print("[*] Server running on port 9999...")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
