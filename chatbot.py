import socket
import threading
import time

# Simple keyword-based offline bot
REPLIES = {
    "hello": "Hi there! 👋",
    "how are you": "I'm just a bot, but I'm doing well!",
    "bye": "Goodbye! Have a great day!",
    "who are you": "I'm your friendly offline chatbot.",
    "thanks": "You're welcome!"
}

HOST = '127.0.0.1'
PORT = 12345
ROOM = 'testroom'

def get_reply(message):
    message = message.lower()
    for keyword in REPLIES:
        if keyword in message:
            return REPLIES[keyword]
    return "I'm not sure how to respond to that."

def main():
    bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        bot.connect((HOST, PORT))
        print("[ChatBot] Connected to server.")
        time.sleep(1)
        bot.send(f"/join {ROOM}".encode())
        print(f"[ChatBot] Joined room '{ROOM}'.")

        while True:
            try:
                msg = bot.recv(1024).decode().strip()
                print(f"[ChatBot] Received: {msg}")
                if any(kw in msg.lower() for kw in REPLIES.keys()):
                    reply = get_reply(msg)
                    time.sleep(1)
                    bot.send(reply.encode())
            except:
                break

    except Exception as e:
        print(f"[ChatBot Error] {e}")
    finally:
        bot.close()

if __name__ == "__main__":
    main()

