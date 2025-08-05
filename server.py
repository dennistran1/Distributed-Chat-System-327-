import socket
import threading
from datetime import datetime
from chatbot import handle_llm_request  # Import real LLM function

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"[STARTED] Server is listening on {HOST}:{PORT}\n")

clients = {}  # socket -> username
chatrooms = {}  # room_name -> set of sockets
client_rooms = {}  # socket -> room_name

lock = threading.Lock()

def broadcast(message, room, sender_socket=None):
    with lock:
        for client in chatrooms.get(room, []):
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    pass

def handle_client(client_socket):
    username = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = username
    client_socket.send("Welcome! Use commands like JOIN #room1, LEAVE, SWITCH #room2".encode('utf-8'))

    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break

            timestamp = datetime.now().strftime("%H:%M:%S")

            if msg.startswith("JOIN "):
                room = msg.split()[1]
                with lock:
                    chatrooms.setdefault(room, set()).add(client_socket)
                    client_rooms[client_socket] = room
                client_socket.send(f"[Joined {room}]".encode('utf-8'))

            elif msg.startswith("SWITCH "):
                room = msg.split()[1]
                with lock:
                    prev_room = client_rooms.get(client_socket)
                    if prev_room and client_socket in chatrooms.get(prev_room, set()):
                        chatrooms[prev_room].remove(client_socket)
                    chatrooms.setdefault(room, set()).add(client_socket)
                    client_rooms[client_socket] = room
                client_socket.send(f"[Switched to {room}]".encode('utf-8'))

            elif msg == "LEAVE":
                with lock:
                    room = client_rooms.pop(client_socket, None)
                    if room:
                        chatrooms[room].remove(client_socket)
                        client_socket.send(f"[Left {room}]".encode('utf-8'))

            elif msg.startswith("/ask"):
                prompt = msg[len("/ask"):].strip()
                response = handle_llm_request(prompt)
                client_socket.send(response.encode('utf-8'))

            elif msg == "exit":
                break

            else:
                room = client_rooms.get(client_socket)
                if room:
                    message = f"[{timestamp}] {username}: {msg}"
                    broadcast(message, room, sender_socket=client_socket)

        except ConnectionResetError:
            break

    with lock:
        room = client_rooms.pop(client_socket, None)
        if room and client_socket in chatrooms.get(room, set()):
            chatrooms[room].remove(client_socket)
        clients.pop(client_socket, None)
        client_socket.close()
        print(f"[DISCONNECTED] {username} left the chat.")


def accept_connections():
    while True:
        client_socket, addr = server.accept()
        print(f"[CONNECTED] {addr} connected.")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

accept_connections()
