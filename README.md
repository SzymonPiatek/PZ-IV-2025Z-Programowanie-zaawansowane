## Projekt z przedmiotu Programowanie Zaawansowane

Prosty system klient–serwer w Pythonie demonstrujący wymianę komunikatów (JSON + binarne dane) oraz serializację obiektów.

---

### 👥 Autorzy
- Tomasz Kowalczyk (nr indeksu: 166186)
- Szymon Piątek (nr indeksu: 166193)

---

### 📁 Struktura projektu
```bash
Zaliczenie/
├── client.py        # Aplikacja kliencka (menu interaktywne)
├── server.py        # Serwer TCP (wielowątkowy)
├── common.py        # Wspólne funkcje I/O (ramkowanie, JSON, bajty)
├── data.py          # Stałe konfiguracyjne i mapowania typów
├── models.py        # Modele danych: Entity, Cat, Dog, Human
├── .client_counter  # Plik licznikowy (tworzony przez klienta)
└── README.md
```

---

### 🚀 Opis działania
- #### Serwer (`server.py`):
  - Nasłuchuje na `HOST`/`PORT` zdefiniowanych w `data.py`.
  - Limit równoczesnych klientów: `MAX_CLIENTS` (domyślnie 2). Po przekroczeniu – odpowiedź `{"status": "REFUSED"}` i rozłączenie.
  - Po przyjęciu połączenia i `{"client_id": ...}` od klienta wysyła `{"status": "OK"}` i obsługuje żądania w pętli.
  - Na żądanie `{"type": "GET", "class": "cat|dog|human"}` wysyła zserializowaną kolekcję obiektów danego typu (lista `Cat|Dog|Human`).

- #### Klient (`client.py`):
  - Generuje trwały `client_id` w pliku `.client_counter` (inkrementowany między uruchomieniami).
  - Łączy się z serwerem i negocjuje status (`OK`/`REFUSED`).
  - Udostępnia interaktywne menu:
    1. Wyświetlanie dostępnych klas (`CLASS_MAP` z `data.py`).
    2. Pobranie kolekcji obiektów wybranego typu i ich wypisanie.
    3. Zakończenie sesji.
 
- #### Wspólne funkcje (`common.py`):
  - Ramkowanie komunikatów 4‑bajtową długością (`struct.pack('!I', size)`).
  - `send_json`/`recv_json` oraz `send_bytes`/`recv_bytes` dla komunikacji.

- #### Modele (`models.py`):
  - Klasa bazowa `Entity` z automatycznym nadawaniem identyfikatorów per typ.
  - Konkretne typy: `Cat`, `Dog`, `Human`.

- #### Konfiguracja (`data.py`):
  - `HOST="127.0.0.1"`, `PORT=5000`, `MAX_CLIENTS=2`.
  - `CLASS_MAP = {"cat": Cat, "dog": Dog, "human": Human}`.

## 🛠 Wymagania
- Python 3.10+ (np. użycie unii typów `socket.socket | None` w kodzie klienta).
- (Opcjonalnie) wirtualne środowisko: `python -m venv .venv && source .venv/bin/activate` (Linux/macOS) lub `.venv\Scripts\activate` (Windows).

## 🏁 Uruchamianie
1. Uruchom serwer w pierwszym terminalu:
   ```bash
   python server.py
   ```
   Serwer wypisze „Server running…” i będzie akceptować połączenia.

2. Uruchom klienta w drugim terminalu:
   ```bash
   python client.py
   ```
   Klient wyświetli status połączenia oraz menu.

3. Zakończ klienta wybierając opcję 3. Serwer zamknie połączenie i zwolni slot klienta.

Uwaga: Jeśli limit `MAX_CLIENTS` zostanie osiągnięty, nowy klient otrzyma `REFUSED` i zakończy działanie.

## 📦 Przegląd plików
- `server.py` – główna logika serwera, obsługa klientów w wątkach, serializacja odpowiedzi.
- `client.py` – klient interaktywny; generacja trwałego `client_id`; walidacja typów odpowiedzi.
- `common.py` – pomocnicze funkcje komunikacyjne (JSON/bajty z nagłówkiem długości).
- `data.py` – konfiguracja hosta/portu, limit klientów, mapowanie nazw klas na typy.
- `models.py` – definicje modeli (`Entity`, `Cat`, `Dog`, `Human`).
- `.client_counter` – plik z licznikiem identyfikatorów klienta (tworzony automatycznie przez klienta).
