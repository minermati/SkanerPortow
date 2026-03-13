import asyncio
import socket
from fastapi import FastAPI

app = FastAPI(title="Recon API")

# Lista popularnych portów do sprawdzenia
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 8080]


# Funkcja asynchroniczna, która sprawdza JEDEN port
async def check_port(ip: str, port: int):
    # Otwieramy połączenie z maksymalnym czasem oczekiwania 1 sekundy (timeout)
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        writer.close()
        await writer.wait_closed()
        return {"port": port, "status": "open"}
    except (asyncio.TimeoutError, ConnectionRefusedError):
        # Jeśli serwer nie odpowie w sekundę lub odrzuci połączenie, port jest zamknięty
        return {"port": port, "status": "closed"}


@app.get("/scan-ports/{domain}")
async def scan_domain_ports(domain: str):
    try:
        # Zamiana nazwy domeny (np. google.com) na adres IP
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return {"error": "Nie można rozwiązać nazwy domeny."}

    # Tworzymy listę "obietnic" (zadań do wykonania w tle)
    tasks = [check_port(ip, port) for port in COMMON_PORTS]

    # Uruchamiamy wszystkie zadania RÓWNOCZEŚNIE (to sprawia, że skaner jest szybki!)
    results = await asyncio.gather(*tasks)

    # Filtrujemy wyniki, żeby zwrócić tylko otwarte porty
    open_ports = [res["port"] for res in results if res["status"] == "open"]

    return {
        "target": domain,
        "ip": ip,
        "open_ports": open_ports
    }