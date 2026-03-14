# 🔍 Web Port Scanner (FastAPI + Vanilla JS)

Nowoczesny, w pełni asynchroniczny skaner portów działający z poziomu przeglądarki. Projekt łączy wydajny backend napisany w Pythonie z responsywnym, minimalistycznym interfejsem użytkownika (UI). 

Aplikacja pozwala na szybkie diagnozowanie otwartych portów na zdalnych serwerach, wykorzystując nieblokujące operacje wejścia/wyjścia, co drastycznie skraca czas skanowania.

## 🚀 Szczegółowy opis funkcji

* **Skanowanie asynchroniczne (Concurrency):** Zamiast sprawdzać porty jeden po drugim, backend wykorzystuje `asyncio` do jednoczesnego uderzania w dziesiątki/setki portów. Dzięki temu skanowanie całego zakresu trwa sekundy, a nie minuty.
* **Rozwiązywanie nazw domenowych (DNS Resolution):** Użytkownik nie musi znać adresu IP. Skaner automatycznie tłumaczy przyjazne nazwy domen (np. `google.com`) na adresy IP przed rozpoczęciem skanowania.
* **Walidacja danych wejściowych:** Backend i Frontend posiadają zabezpieczenia sprawdzające, czy podany adres IP lub domena mają poprawny format, zapobiegając błędom aplikacji.
* **Identyfikacja popularnych usług:** Skaner nie tylko zwraca numer otwartego portu (np. `80`, `443`), ale również podpowiada, jaka usługa prawdopodobnie za nim stoi (np. `HTTP`, `HTTPS`, `FTP`, `SSH`).
* **Skanowanie popularnych portów vs. Pełny zakres:** Możliwość szybkiego przeskanowania najważniejszych portów (top 100/1000) lub zdefiniowania własnego zakresu.
* **Real-time UI (Dynamiczne renderowanie):** Wyniki pojawiają się na ekranie natychmiast po otrzymaniu odpowiedzi z serwera, bez konieczności odświeżania strony (wykorzystanie `Fetch API`).
* **Obsługa błędów (Error Handling):** Aplikacja elegancko radzi sobie z timeoutami, odrzuconymi połączeniami (Connection Refused) i błędnymi adresami, wyświetlając czytelne komunikaty dla użytkownika (np. "Host nieosiągalny").

## 🛠️ Technologie i Architektura

Projekt został zbudowany w architekturze **Client-Server** z podziałem na warstwy:

**Backend (Logika i Sieć):**
* **Python 3.13+**
* **FastAPI** - framework do budowy API, wybrany ze względu na natywne wsparcie dla asynchroniczności i ogromną szybkość.
* **Uvicorn** - lekki i błyskawiczny serwer ASGI.
* Wbudowane biblioteki `socket` oraz `asyncio` do niskopoziomowej komunikacji sieciowej TCP.

**Frontend (Prezentacja):**
* **HTML5 & CSS3** - Nowoczesny układ oparty na CSS Grid i Flexbox.
* **Vanilla JavaScript** - Czysty JS bez ciężkich frameworków (React/Vue), co gwarantuje natychmiastowe ładowanie strony. Zastosowano nowoczesną składnię `async/await`.

https://skanerportow.onrender.com
   
