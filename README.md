# 📌 Projekt z przedmiotu Programowanie Zaawansowane

Repozytorium projektu z przedmiotu Programowanie Zaawansowane (PZ-IV-2025Z) — klient-serwer w Pythonie.

Autorzy

## 📁 Struktura projektu
```bash
PZ-IV-2025Z-Programowanie-zaawansowane/
├── client.py        # Kod klienta
├── server.py        # Kod serwera
├── common.py        # Wspólne funkcje/moduły
├── data.py          # Warstwa dostępu do danych
├── models.py        # Modele danych
├── .gitignore
└── README.md
```

## 🚀 Opis

Projekt implementuje prosty system klient-serwer w Pythonie. Celem jest przedstawienie mechanizmów komunikacji między procesami oraz podstawowej architektury aplikacji z podziałem na:

- Warstwę serwera (server.py)

- Warstwę klienta (client.py)

- Wspólne komponenty (common.py)

- Modele danych (models.py)

- Logikę zarządzania danymi (data.py)

## 🛠 Wymagania

Python 3.8+*

(Opcjonalnie) wirtualne środowisko

## 🏁 Uruchamianie

### 🔹 Serwer

Otwórz terminal

Przejdź do katalogu projektu

Uruchom:
```bash
python server.py
```

Serwer powinien zacząć nasłuchiwać żądań od klientów.

### 🔹 Klient

W osobnym terminalu:
```bash
python client.py
```

Klient łączy się z serwerem i wykonuje zdefiniowane operacje (np. wysyła zapytania, odbiera dane).

### 📝 Upewnij się, że serwer działa zanim uruchomisz klienta.

## 📦 Moduły

### Plik	    
- server.py - Główna logika serwera, nasłuchiwanie i obsługa połączeń
- client.py	- Klient komunikujący się z serwerem
- common.py	- Funkcje i klasy wspólne dla klienta i serwera
- data.py	- Logika operacji na danych (np. CRUD, zmiana liczby klientów)
- models.py	- Definicje modeli danych
