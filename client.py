import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{timestamp}] {message}\n> ", end='')
        except:
            print("\n[ERROR] Connection closed by server.")
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
        except:
            print("[ERROR] Unable to connect to server.")
            return

        username = input("Enter your username: ")
        client_socket.send(username.encode('utf-8'))

        # Start thread to listen for messages
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

        print("\n[CONNECTED] You can now chat!")
        print("Type JOIN #room, SWITCH #room, LEAVE, /ask <question>, or exit to quit.\n")

        while True:
            msg = input("> ")
            if msg.lower() == 'exit':
                client_socket.send(b"exit")
                break
            try:
                client_socket.send(msg.encode('utf-8'))
            except:
                print("[ERROR] Failed to send message.")
                break

if __name__ == '__main__':
    main()
