import socket
import threading
import time
import openai

# ==== CONFIGURATION ====
HOST = '127.0.0.1'
PORT = 12345
ROOM = 'testroom'
USERNAME = 'chatbot'

# ==== OpenRouter Setup ====
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

def ask_llm(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM Error] {e}"

def main():
    bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        bot.connect((HOST, PORT))
        print("[ChatBot] Connected to server.")
        time.sleep(1)

        # Auto register (just in case)
        bot.sendall(f"/register {USERNAME}\n".encode())
        time.sleep(1)

        # Login
        bot.sendall(f"/login {USERNAME}\n".encode())
        time.sleep(1)

        # Join room
        bot.sendall(f"/join {ROOM}\n".encode())
        print(f"[ChatBot] Logged in and joined room '{ROOM}'.")

        while True:
            try:
                msg = bot.recv(1024).decode().strip()
                print(f"[ChatBot] Received: {msg}")

                # Ignore server errors to avoid bot loops
                if msg.startswith("❌") or msg.startswith("⚠️") or not msg:
                    continue

                reply = ask_llm(msg)
                time.sleep(1)
                bot.sendall(reply.encode())

            except Exception as e:
                print(f"[ChatBot Error] {e}")
                break

    except Exception as e:
        print(f"[ChatBot Connection Error] {e}")
    finally:
        bot.close()

if __name__ == "__main__":
    main()
