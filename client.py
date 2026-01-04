import socket
import pickle
import os

from common import send_json, recv_json, recv_bytes
from data import HOST, PORT, CLASS_MAP


class ClientIdCounter:
    """
    Persistent client ID generator.

    This class is responsible for generating unique client identifiers
    that persist across multiple executions of the client program.
    The identifier value is stored in a local file, which allows the
    counter to survive process termination.

    This mechanism is conceptually equivalent to a static counter used
    in the Entity class on the server side, but with persistence.
    """

    FILE = ".client_counter"

    @classmethod
    def next_id(cls) -> int:
        if not os.path.exists(cls.FILE):
            with open(cls.FILE, "w") as f:
                f.write("1")
            return 1

        with open(cls.FILE, "r+") as f:
            value = int(f.read())
            new_value = value + 1
            f.seek(0)
            f.write(str(new_value))
            f.truncate()
            return new_value


class Client:
    _counter = 0

    def __init__(self):
        self.client_id = ClientIdCounter.next_id()
        self.socket: socket.socket | None = None

    def connect(self) -> None:
        """
        Establishes a connection with the server.

        Sends the client ID to the server and receives a connection status.
        If the server responds with REFUSED, the client terminates execution.
        If the response is OK, the client enters an active session.

        :raises SystemExit: If the connection is refused.
        :raises RuntimeError: If an unknown server status is received.
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        send_json(self.socket, {"client_id": self.client_id})
        response = recv_json(self.socket)

        status = response.get("status")

        if status == "REFUSED":
            print(f"[client {self.client_id}] STATUS = REFUSED")
            self.socket.close()
            raise SystemExit

        if status != "OK":
            raise RuntimeError(f"Nieznany status serwera: {status}")

        print(f"[client {self.client_id}] STATUS = OK – połączono")

    def show_menu(self) -> None:
        """
        Displays the interactive menu options to the user.

        Available options:
        - display available classes,
        - request an object collection,
        - terminate the client session.
        """

        print("\n=== MENU ===")
        print("1. Wyświetl spis klas")
        print("2. Poproś o mapę obiektów")
        print("3. Zakończ sesję")

    def show_classes(self) -> None:
        """
        Displays the list of available object classes
        that can be requested from the server.
        """

        print("\nDostępne klasy:")
        for cls in CLASS_MAP.keys():
            print(f"- {cls}")

    def request_objects(self, cls: str) -> None:
        """
        Requests a collection of objects of a given class from the server.

        The method:
        - sends a request specifying the class name,
        - receives serialized data from the server,
        - deserializes the data,
        - validates the received object types,
        - prints the objects in a streaming manner.

        If the server sends an object of an unexpected type,
        the method handles the type casting error as required
        by the project specification.

        :param cls: Name of the requested class (lowercase)
        """

        assert self.socket is not None

        send_json(self.socket, {"type": "GET", "class": cls})
        raw = recv_bytes(self.socket)

        try:
            data = pickle.loads(raw)
            expected_type = CLASS_MAP.get(cls)

            if not isinstance(data, list):
                raise TypeError(
                    f"Oczekiwano kolekcji (listy), otrzymano {type(data).__name__}"
                )

            for obj in data:
                if not isinstance(obj, expected_type):
                    raise TypeError(
                        f"Nie można zrzutować {type(obj).__name__} "
                        f"na {expected_type.__name__}"
                    )
                print(f"[client {self.client_id}] {obj}")

        except Exception as e:
            print(f"[client {self.client_id}] BŁĄD ({cls}): {e}")

    def run(self) -> None:
        """
        Starts the client execution.

        After successfully connecting to the server, the client enters
        an interactive session loop where the user can repeatedly
        perform actions until choosing to exit.
        """

        self.connect()

        while True:
            self.show_menu()
            choice = input("Wybierz opcję: ").strip()

            if choice == "1":
                self.show_classes()

            elif choice == "2":
                cls = input("Podaj nazwę klasy: ").strip().lower()

                if cls not in CLASS_MAP:
                    print("Nieznana klasa")
                    continue

                self.request_objects(cls)

            elif choice == "3":
                self.disconnect()
                break

            else:
                print("Nieprawidłowa opcja")

    def disconnect(self) -> None:
        """
        Gracefully terminates the client session.

        Sends a termination message to the server, closes the socket,
        and releases all client-side resources.
        """

        if self.socket:
            try:
                send_json(self.socket, {"type": "BYE"})
            except Exception:
                pass
            self.socket.close()

        print(f"[client {self.client_id}] DISCONNECTED")


if __name__ == "__main__":
    Client().run()
