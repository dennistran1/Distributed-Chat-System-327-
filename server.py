import socket
import threading
from chatroom import ChatRoomManager

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

chatrooms = ChatRoomManager()
clients = []

print(f"[STARTED] Server listening on {HOST}:{PORT}")

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    client_socket.send(
        "Welcome to the chat server!\n"
        "Use /join <room>, /leave, /list, or just type to chat.\n".encode()
    )

    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break

            if message.startswith("/join"):
                parts = message.split()
                if len(parts) == 2:
                    room_name = parts[1]
                    chatrooms.join_room(client_socket, room_name)
                    client_socket.send(f"Joined room '{room_name}'\n".encode())
                else:
                    client_socket.send("Usage: /join <room_name>\n".encode())

            elif message.startswith("/leave"):
                chatrooms.leave_room(client_socket)
                client_socket.send("Left the chatroom.\n".encode())

            elif message.startswith("/list"):
                rooms = chatrooms.list_rooms()
                if rooms:
                    client_socket.send(f"Available rooms: {', '.join(rooms)}\n".encode())
                else:
                    client_socket.send("No active chatrooms.\n".encode())

            elif message.startswith("/quit"):
                break

            else:
                chatrooms.broadcast(client_socket, f"{address}: {message}")

        except ConnectionResetError:
            break

    print(f"[DISCONNECTED] {address} disconnected.")
    chatrooms.leave_room(client_socket)
    client_socket.close()

def receive_connections():
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

receive_connections()
