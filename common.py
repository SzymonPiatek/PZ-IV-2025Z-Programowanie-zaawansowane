import json
import struct
import socket


def send_json(sock: socket.socket, data: dict) -> None:
    payload = json.dumps(data).encode()
    sock.sendall(struct.pack("!I", len(payload)))
    sock.sendall(payload)


def recv_json(sock: socket.socket) -> dict:
    size = struct.unpack("!I", sock.recv(4))[0]
    payload = sock.recv(size)
    return json.loads(payload.decode())


def send_bytes(sock: socket.socket, data: bytes) -> None:
    sock.sendall(struct.pack("!I", len(data)))
    sock.sendall(data)


def recv_bytes(sock: socket.socket) -> bytes:
    size = struct.unpack("!I", sock.recv(4))[0]
    return sock.recv(size)
