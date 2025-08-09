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

        # Auto register and login
        bot.sendall(f"/register {USERNAME}\n".encode())
        time.sleep(1)
        bot.sendall(f"/login {USERNAME}\n".encode())
        time.sleep(1)
        bot.sendall(f"/join {ROOM}\n".encode())
        print(f"[ChatBot] Logged in and joined room '{ROOM}'.")

        while True:
            try:
                msg = bot.recv(1024).decode().strip()
                print(f"[ChatBot] Received: {msg}")

                # Ignore errors, empty messages, or own messages
                if not msg or msg.startswith("❌") or msg.startswith("⚠️"):
                    continue
                if msg.startswith(f"{USERNAME}:"):
                    continue

                # Only respond to messages starting with /ask
                if "/ask" not in msg.lower():
                    continue

                # Extract question
                question = msg.lower().split("/ask", 1)[1].strip()
                if not question:
                    continue

                reply = ask_llm(question)
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

