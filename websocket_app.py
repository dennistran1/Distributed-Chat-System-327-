
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

CHAT_SERVER_HOST = '127.0.0.1'
CHAT_SERVER_PORT = 12345

# Create a persistent client connection (shared across requests)
persistent_client = {
    'socket': None,
    'lock': threading.Lock()
}

def connect_to_server():
    if persistent_client['socket'] is None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((CHAT_SERVER_HOST, CHAT_SERVER_PORT))
        persistent_client['socket'] = s
        try:
            welcome = s.recv(1024).decode()
            socketio.emit('server_message', {'message': welcome})
        except:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_send_message(data):
    message = data['message']
    emit('user_message', {'message': message}, broadcast=False)

    def handle_server_response():
        try:
            connect_to_server()
            with persistent_client['lock']:
                s = persistent_client['socket']
                s.send((message + "\n").encode())
                s.settimeout(1.0)
                response = ""
                try:
                    while True:
                        chunk = s.recv(1024).decode()
                        if not chunk:
                            break
                        response += chunk
                except socket.timeout:
                    pass
                socketio.emit('server_message', {'message': response or "[No response from server]"})

        except Exception as e:
            socketio.emit('server_message', {'message': f"[Connection error] {e}"})

    threading.Thread(target=handle_server_response).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5050)
