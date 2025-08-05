# Distributed-Chat-System-327-

Overview

This is a basic distributed chat system written in Python. It allows multiple clients to connect to a central server, join chatrooms, exchange messages, and optionally query an AI assistant using /ask. The system demonstrates key distributed systems concepts including message passing, concurrency (via threading), and basic performance measurement.

Features

Multi-client chat via TCP sockets

Multi-chatroom support (JOIN, SWITCH, LEAVE)

Message broadcasting within chatrooms

Optional AI assistant command: /ask <question>

Message timestamps for latency analysis

Setup Instructions

Requirements

Python 3.10+

(Optional) openai and python-dotenv if integrating LLM chatbot

Install Dependencies (optional for LLM)

pip install openai python-dotenv

File Structure

chat-system/
├── server.py              # Server-side logic
├── client.py              # Terminal-based client
├── chatbot.py             # (Optional) LLM assistant module
├── test_simulation.py     # (Optional) Performance test script
├── messages.log           # Log file (optional)
├── README.md

Running the System

1. Start the Server

python server.py

2. Start Clients (In separate terminals)

python client.py

3. Use Commands in Client

JOIN #room1 – Join or create a room

SWITCH #room2 – Move to another room

LEAVE – Leave current room

/ask What is a distributed system? – (Optional) Ask the LLM bot

exit – Disconnect from chat

Notes

You can run multiple clients from different terminals.

Each chatroom is isolated: clients only see messages from their current room.

Server logs client joins, messages, and disconnections.

LLM support can be added later in chatbot.py and integrated into server.py.


Author

Dennis Tran]CECS 327 – Networks and Distributed Computing
