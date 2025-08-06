
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 12345
NUM_CLIENTS = 5
NUM_MESSAGES = 10
latencies = []

def client_simulation(client_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.recv(1024)  # Welcome message

        # Join chatroom using valid command
        sock.send(b"/join testroom")
        sock.recv(1024)

        for i in range(NUM_MESSAGES):
            msg = f"Message {i} from SimClient{client_id}"
            start_time = time.time()
            sock.send(msg.encode())
            time.sleep(0.1)  # simulate message delay
            latency = (time.time() - start_time) * 1000  # in ms
            latencies.append(latency)

        sock.send(b"/quit")
        sock.close()
    except Exception as e:
        print(f"[Client {client_id} Error] {e}")

def run_simulation():
    threads = []
    for i in range(NUM_CLIENTS):
        thread = threading.Thread(target=client_simulation, args=(i,))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    # Write latency results to a file
    with open("latency_data.txt", "w") as f:
        for latency in latencies:
            f.write(f"{latency}\n")

    print(f"[Simulation Complete] {len(latencies)} messages sent.")
    print("[Data written to latency_data.txt]")

if __name__ == "__main__":
    run_simulation()

