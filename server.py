import socket
import threading
import sqlite3
from chatroom import ChatRoomManager
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

chatrooms = ChatRoomManager()
clients = []
logged_in_users = {}

# === SQLite Setup ===
conn = sqlite3.connect('chat.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    room TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
""")

conn.commit()

print(f"[STARTED] Server listening on {HOST}:{PORT}")

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    client_socket.send(
        "Welcome to the chat server!\n"
        "Use /register <name>, /login <name>, /join <room>, /leave, /list, /history, or /quit.\n".encode()
    )

    current_room = None

    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break

            # === Register ===
            if message.startswith("/register"):
                parts = message.split()
                if len(parts) == 2:
                    username = parts[1]
                    try:
                        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
                        conn.commit()
                        client_socket.send(f"✅ Registered as '{username}'\n".encode())
                    except sqlite3.IntegrityError:
                        client_socket.send(f"⚠️ Username '{username}' is already taken.\n".encode())
                else:
                    client_socket.send("Usage: /register <username>\n".encode())

            # === Login ===
            elif message.startswith("/login"):
                parts = message.split()
                if len(parts) == 2:
                    username = parts[1]
                    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                    if cursor.fetchone():
                        logged_in_users[client_socket] = username
                        client_socket.send(f"✅ Logged in as '{username}'\n".encode())
                    else:
                        client_socket.send(f"❌ Username '{username}' not found.\n".encode())
                else:
                    client_socket.send("Usage: /login <username>\n".encode())

            # === Join Room (login required) ===
            elif message.startswith("/join"):
                if client_socket not in logged_in_users:
                    client_socket.send("❌ Please login first with /login <username>\n".encode())
                    continue

                parts = message.split()
                if len(parts) == 2:
                    current_room = parts[1]
                    chatrooms.join_room(client_socket, current_room)
                    client_socket.send(f"Joined room '{current_room}'\n".encode())
                else:
                    client_socket.send("Usage: /join <room_name>\n".encode())

            # === Leave Room ===
            elif message.startswith("/leave"):
                chatrooms.leave_room(client_socket)
                current_room = None
                client_socket.send("Left the chatroom.\n".encode())

            # === List Rooms ===
            elif message.startswith("/list"):
                rooms = chatrooms.list_rooms()
                if rooms:
                    client_socket.send(f"Available rooms: {', '.join(rooms)}\n".encode())
                else:
                    client_socket.send("No active chatrooms.\n".encode())

            # === Show History (login required) ===
            elif message.startswith("/history"):
                if client_socket not in logged_in_users:
                    client_socket.send("❌ Please login to view chat history.\n".encode())
                    continue
                if not current_room:
                    client_socket.send("❌ Join a room to view its history.\n".encode())
                    continue

                cursor.execute("""
                    SELECT sender, content, timestamp FROM messages
                    WHERE room = ?
                    ORDER BY id DESC LIMIT 10
                """, (current_room,))
                rows = cursor.fetchall()
                if rows:
                    history = "\n".join([f"[{r[2]}] {r[0]}: {r[1]}" for r in reversed(rows)])
                    client_socket.send(f"Last 10 messages in '{current_room}':\n{history}\n".encode())
                else:
                    client_socket.send(f"No messages in '{current_room}'.\n".encode())

            # === Quit ===
            elif message.startswith("/quit"):
                break

            # === Regular Messages (only if logged in & in a room) ===
            else:
                if client_socket not in logged_in_users:
                    client_socket.send("❌ Please login before chatting.\n".encode())
                    continue
                if not current_room:
                    client_socket.send("❌ Join a room to send messages.\n".encode())
                    continue

                sender = logged_in_users[client_socket]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO messages (sender, room, content, timestamp) VALUES (?, ?, ?, ?)",
                               (sender, current_room, message, timestamp))
                conn.commit()
                chatrooms.broadcast(client_socket, f"{sender}: {message}")

        except ConnectionResetError:
            break

    print(f"[DISCONNECTED] {address} disconnected.")
    chatrooms.leave_room(client_socket)
    client_socket.close()
    if client_socket in logged_in_users:
        del logged_in_users[client_socket]

def receive_connections():
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

receive_connections()

