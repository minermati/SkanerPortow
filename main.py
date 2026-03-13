import asyncio
import socket
import httpx
from fastapi import FastAPI

app = FastAPI(title="Recon API", description="Narzędzie do rekonensansu w FastAPI")

# ==========================================
# KONFIGURACJA SKANERA
# ==========================================
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 8080]

COMMON_PATHS = [
    "admin", "login", "robots.txt", "backup", "db",
    ".git", ".env", "api", "config", "test"
]


# ==========================================
# STRONA GŁÓWNA
# ==========================================
@app.get("/")
def read_root():
    return {"message": "Recon API działa! Przejdź pod /docs, aby testować."}


# ==========================================
# MODUŁ 1: SKANER PORTÓW
# ==========================================
async def check_port(ip: str, port: int):
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        writer.close()
        await writer.wait_closed()
        return {"port": port, "status": "open"}
    except (asyncio.TimeoutError, ConnectionRefusedError):
        return {"port": port, "status": "closed"}
    except Exception:
        return {"port": port, "status": "error"}


@app.get("/scan-ports/{domain}")
async def scan_domain_ports(domain: str):
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return {"error": "Nie można rozwiązać nazwy domeny."}

    tasks = [check_port(ip, port) for port in COMMON_PORTS]
    results = await asyncio.gather(*tasks)
    open_ports = [res["port"] for res in results if res.get("status") == "open"]

    return {
        "target": domain,
        "ip": ip,
        "open_ports": open_ports
    }


# ==========================================
# MODUŁ 2: ENUMERACJA SUBDOMEN (OSINT)
# ==========================================
@app.get("/scan-subdomains/{domain}")
async def get_subdomains(domain: str):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=15.0)
            if response.status_code != 200:
                return {"error": "Baza certyfikatów jest obecnie niedostępna."}

            data = response.json()
            subdomains = set()
            for entry in data:
                name = entry['name_value'].lower()
                if "\n" in name:
                    subdomains.update(name.split("\n"))
                else:
                    subdomains.add(name)

            return {
                "target": domain,
                "count": len(subdomains),
                "subdomains": sorted(list(subdomains))
            }
        except Exception as e:
            return {"error": f"Błąd: {str(e)}"}


# ==========================================
# MODUŁ 3: FUZZING KATALOGÓW
# ==========================================
async def check_path(client: httpx.AsyncClient, base_url: str, path: str):
    url = f"{base_url}/{path}"
    try:
        response = await client.get(url, timeout=3.0)
        if response.status_code != 404:
            return {"url": url, "status": response.status_code}
    except httpx.RequestError:
        pass
    return None


@app.get("/scan-directories/{domain}")
async def scan_directories(domain: str):
    # Domyślnie sprawdzamy po HTTP, żeby było szybciej
    base_url = f"http://{domain}"

    async with httpx.AsyncClient() as client:
        tasks = [check_path(client, base_url, path) for path in COMMON_PATHS]
        results = await asyncio.gather(*tasks)
        found_paths = [res for res in results if res is not None]

    return {
        "target": domain,
        "found_directories": found_paths
    }