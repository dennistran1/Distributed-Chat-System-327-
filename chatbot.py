
import socket
import threading
import time
import openai
import os

# ==== CONFIGURATION ====
HOST = '127.0.0.1'
PORT = 12345
ROOM = 'testroom'

# ==== OpenRouter Setup ====
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

def ask_llm(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # You can also try "anthropic/claude-3-haiku"
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
        bot.send(f"/join {ROOM}".encode())
        print(f"[ChatBot] Joined room '{ROOM}'.")

        while True:
            try:
                msg = bot.recv(1024).decode().strip()
                print(f"[ChatBot] Received: {msg}")

                if msg:
                    time.sleep(1)
                    reply = ask_llm(msg)
                    bot.send(reply.encode())

            except Exception as e:
                print(f"[ChatBot Error] {e}")
                break

    except Exception as e:
        print(f"[ChatBot Connection Error] {e}")
    finally:
        bot.close()

if __name__ == "__main__":
    main()
