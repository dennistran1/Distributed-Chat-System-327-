
# chatroom.py

from threading import Lock

class ChatRoomManager:
    def __init__(self):
        self.rooms = {}  # room_name: list of client sockets
        self.client_rooms = {}  # client socket: room_name
        self.lock = Lock()

    def join_room(self, client_socket, room_name):
        with self.lock:
            if room_name not in self.rooms:
                self.rooms[room_name] = []
            if client_socket not in self.rooms[room_name]:
                self.rooms[room_name].append(client_socket)
            self.client_rooms[client_socket] = room_name

    def leave_room(self, client_socket):
        with self.lock:
            room = self.client_rooms.get(client_socket)
            if room:
                self.rooms[room].remove(client_socket)
                if not self.rooms[room]:
                    del self.rooms[room]
                del self.client_rooms[client_socket]

    def get_room(self, client_socket):
        with self.lock:
            return self.client_rooms.get(client_socket)

    def list_rooms(self):
        with self.lock:
            return list(self.rooms.keys())

    def broadcast(self, sender_socket, message):
        with self.lock:
            room = self.client_rooms.get(sender_socket)
            if room:
                for client in self.rooms[room]:
                    if client != sender_socket:
                        try:
                            client.send(message.encode())
                        except:
                            pass  # ignore broken clients
