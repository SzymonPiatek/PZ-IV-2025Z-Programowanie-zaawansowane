import socket
import threading
import pickle
import random
import time

from models import Cat, Dog, Human
from common import send_json, recv_json, send_bytes
from data import HOST, PORT, MAX_CLIENTS


clients_lock = threading.Lock()
active_clients = 0

entities = [
    *[Cat(name) for name in ["Mruczek", "Luna", "Kleo", "Filemon"]],
    *[Dog(name) for name in ["Reksio", "Azor", "Burek", "Nero"]],
    *[Human(name) for name in ["Adam", "Ewa", "Jan", "Anna"]],
]

object_map = {e.key(): e for e in entities}


def handle_client(conn: socket.socket, addr):
    """
    Handles communication with a single connected client.

    This function is executed in a separate thread for each client.
    It performs the following steps:
    - receives the client identifier,
    - checks whether the maximum number of clients has been reached,
    - sends connection status (`OK` or `REFUSED`),
    - processes client requests in a loop,
    - sends serialized object collections or a random object if no match exists,
    - logs all actions to the console.

    :param conn: Socket connected to the client.
    :param addr: Client address.
    """

    global active_clients

    client_ip, client_port = addr

    try:
        hello = recv_json(conn)
        client_id = hello["client_id"]

        with clients_lock:
            if active_clients >= MAX_CLIENTS:
                send_json(conn, {"status": "REFUSED"})
                print(f"[REFUSED] client {client_id} from {client_ip}:{client_port} - max clients reached")
                return
            active_clients += 1

        send_json(conn, {"status": "OK"})
        print(f"[CONNECTED] client {client_id} from {client_ip}:{client_port}")

        while True:
            req = recv_json(conn)
            if req["type"] == "BYE":
                break

            requested = req["class"].lower()
            time.sleep(random.uniform(0.2, 0.8))

            result = [
                obj for key, obj in object_map.items()
                if key.startswith(requested)
            ]

            if not result:
                obj = random.choice(list(object_map.values()))
                data = pickle.dumps(obj)
                send_bytes(conn, data)
                print(f"[SEND RANDOM] to client {client_id}: {obj}")
            else:
                data = pickle.dumps(result)
                send_bytes(conn, data)
                print(f"[SEND] to client {client_id}: {[str(o) for o in result]}")
    finally:
        with clients_lock:
            active_clients -= 1
        conn.close()
        print(f"[DISCONNECTED] client {client_id}")


def start_server():
    """
    Starts the TCP server and listens for incoming client connections.

    For each accepted connection, a new daemon thread is created
    to handle communication with the client.

    The server runs indefinitely until the process is terminated.
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server running...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
