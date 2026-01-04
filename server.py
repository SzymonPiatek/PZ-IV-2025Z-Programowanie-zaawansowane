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
    Cat("Mruczek"),
    Cat("Luna"),
    Cat("Kleo"),
    Cat("Filemon"),

    Dog("Reksio"),
    Dog("Azor"),
    Dog("Burek"),
    Dog("Nero"),

    Human("Adam"),
    Human("Ewa"),
    Human("Jan"),
    Human("Anna"),
]

object_map = {e.key(): e for e in entities}


def handle_client(conn: socket.socket, addr):
    global active_clients

    try:
        hello = recv_json(conn)
        client_id = hello["client_id"]

        with clients_lock:
            if active_clients >= MAX_CLIENTS:
                send_json(conn, {"status": "REFUSED"})
                print(f"[REFUSED] client {client_id}")
                return
            active_clients += 1

        send_json(conn, {"status": "OK"})
        print(f"[CONNECTED] client {client_id}")

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server running...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
