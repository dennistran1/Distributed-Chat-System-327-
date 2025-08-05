import socket
import threading
import time
import statistics

HOST = '127.0.0.1'
PORT = 12345
NUM_CLIENTS = 5
NUM_MESSAGES = 10

latencies = []

def client_simulation(client_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(f"SimClient{client_id}".encode('utf-8'))
        sock.recv(1024)  # Welcome message
        sock.send(b"JOIN #test")
        sock.recv(1024)

        for i in range(NUM_MESSAGES):
            msg = f"Message {i} from SimClient{client_id}"
            start_time = time.time()
            sock.send(msg.encode('utf-8'))
            # Optionally wait for response from another client (not expected here)
            time.sleep(0.1)
            latency = (time.time() - start_time) * 1000  # ms
            latencies.append(latency)

        sock.send(b"exit")
        sock.close()
    except Exception as e:
        print(f"[Client {client_id} Error] {e}")

def run_simulation():
    threads = []
    for i in range(NUM_CLIENTS):
        thread = threading.Thread(target=client_simulation, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\n--- Simulation Complete ---")
    print(f"Total messages sent: {NUM_CLIENTS * NUM_MESSAGES}")
    print(f"Average latency: {statistics.mean(latencies):.2f} ms")
    print(f"Max latency: {max(latencies):.2f} ms")
    print(f"Min latency: {min(latencies):.2f} ms")

if __name__ == '__main__':
    run_simulation()
