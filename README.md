
# Distributed Multi-Chatroom Messaging System

This is a distributed messaging system built in Python using sockets and threading. It supports multiple clients, chatrooms, a chatbot powered by OpenRouter (GPT-3.5), and includes performance analysis with latency visualization.

---

## 🔧 Features

- 🧠 **Multi-client, multi-threaded server** using TCP sockets
- 💬 **Multiple chatrooms** with command support:
  - `/join <room>` — join or create a chatroom
  - `/leave` — leave current room
  - `/list` — show all active chatrooms
  - `/quit` — disconnect
- 🤖 **Chatbot (AI-enhanced)** that responds intelligently using the OpenRouter API (GPT-3.5)
- 📊 **Performance testing** with `testsimulation.py` simulating client load
- 📈 **Latency plot** generated with `latency_plot.py` (outputs `latency_plot.png`)
- 🧪 **Latency data file**: `latency_data.txt`
- 📦 **SQLite database** stores user accounts and chat messages

---

## 📁 File Structure

```
DistributedChat327/
│
├── server.py # Multi-threaded server
├── client.py # User-facing chat client
├── chatroom.py # Chatroom management logic
├── chatbot.py # Chatbot using OpenRouter API
├── testsimulation.py # Simulates multiple clients and records latency
├── latency_plot.py # Plots latency data into latency_plot.png
├── latency_data.txt # Raw latency results from simulation
├── latency_plot.png # Visualized latency graph
├── chat.db # SQLite database with user/message logs
├── web_frontend/ # WebSocket frontend with Flask
└── README.md # You're here
```

---

## 🚀 How to Run

### Terminal Tab 1: Start Server
```bash
python3 server.py
```

### Terminal Tab 2: Client 1
```bash
python3 client.py
/join testroom
hello
```

### Terminal Tab 3: Client 2
```bash
python3 client.py
/join testroom
how are you?
```

### Terminal Tab 4: Chatbot (AI-Powered)
```bash
python3 chatbot.py
```

- Make sure you insert your OpenRouter API key in `chatbot.py`:
```python
openai.api_key = "sk-or-XXXXXXXXXXXXXXXXXXXXXXXX"
openai.api_base = "https://openrouter.ai/api/v1"
```

### Terminal Tab 5: Load Test + Latency Plot
```bash
python3 testsimulation.py
python3 latency_plot.py
open latency_plot.png
```
## 🌐 Web Frontend (Real-Time Chat)

To run the browser-based chat:

1. Make sure `server.py` is running
2. Start the frontend:
   ```bash
   cd web_frontend
   python3 websocket_app.py --port=5050

## 📦 Database (SQLite)
The system uses a lightweight SQLite database (chat.db) to persist:

✅ Registered user accounts

💬 Message history by chatroom

📅 Timestamps for each message

📂 Tables
users

id (INT, Primary Key)

username (TEXT, Unique)

messages

id (INT, Primary Key)

sender (TEXT)

room (TEXT)

content (TEXT)

timestamp (TEXT)

🧪 How to View Your Data
1. Run this in Terminal from your project folder:

bash
Copy
Edit
sqlite3 chat.db
Inside the SQLite prompt:

sql
Copy
Edit
.tables
SELECT * FROM users;
SELECT * FROM messages ORDER BY id DESC LIMIT 10;
.exit

---

## 📡 API Notes

This project uses [OpenRouter.ai](https://openrouter.ai) to access GPT-3.5-level models
