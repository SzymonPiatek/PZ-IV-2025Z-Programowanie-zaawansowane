import json
import struct
import socket


def send_json(sock: socket.socket, data: dict) -> None:
    """
    Sends a dictionary as a JSON message over a TCP socket.

    The message is serialized to JSON, encoded as UTF-8 bytes,
    and prefixed with a 4-byte length header.

    :param sock: An active TCP socket
    :param data: Dictionary to be sent
    """

    payload = json.dumps(data).encode()
    sock.sendall(struct.pack("!I", len(payload)))
    sock.sendall(payload)


def recv_json(sock: socket.socket) -> dict:
    """
    Receives a JSON message from a TCP socket.

    Reads the 4-byte length header first, then reads the specified
    number of bytes and decodes them into a Python dictionary.

    :param sock: An active TCP socket
    :return: Decoded JSON object as a dictionary
    """

    size = struct.unpack("!I", sock.recv(4))[0]
    payload = sock.recv(size)
    return json.loads(payload.decode())


def send_bytes(sock: socket.socket, data: bytes) -> None:
    """
    Sends raw binary data over a TCP socket.

    The data is prefixed with a 4-byte length header.

    :param sock: An active TCP socket
    :param data: Raw bytes to be sent
    """

    sock.sendall(struct.pack("!I", len(data)))
    sock.sendall(data)


def recv_bytes(sock: socket.socket) -> bytes:
    """
    Receives raw binary data from a TCP socket.

    Reads the 4-byte length header first, then reads the specified
    number of bytes from the socket.

    :param sock: An active TCP socket
    :return: Received raw bytes
    """

    size = struct.unpack("!I", sock.recv(4))[0]
    return sock.recv(size)
