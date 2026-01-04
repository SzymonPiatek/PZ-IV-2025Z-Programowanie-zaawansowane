from models import Cat, Dog, Human


HOST = "127.0.0.1"
PORT = 5000

MAX_CLIENTS = 2

CLASS_MAP = {
    "cat": Cat,
    "dog": Dog,
    "human": Human
}
