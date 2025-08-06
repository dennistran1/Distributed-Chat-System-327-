
import socket
import threading
import time

# Extended keyword-based offline bot
REPLIES = {
    "hello": "Hi there! 👋",
    "how are you": "I'm just a bot, but I'm doing well!",
    "bye": "Goodbye! Have a great day!",
    "who are you": "I'm your friendly offline chatbot.",
    "thanks": "You're welcome!",
    "joke": "Why did the programmer quit his job? Because he didn't get arrays.",
    "help": "Try asking me about the weather, a joke, or how I am!",
    "weather": "It's always sunny in the terminal. ☀️",
    "study tip": "Break your work into small chunks and take regular breaks!",
    "exam": "Good luck! Remember to breathe and stay focused.",
    "chatroom": "Chatrooms help separate conversations into isolated spaces.",
    "project": "Sounds like you're building something awesome!",
    "python": "Python is a powerful language for distributed systems.",
    "bot": "Yes, I'm a bot! And proud of it."
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
