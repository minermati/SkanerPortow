from fastapi import FastAPI
from fastapi.responses import FileResponse  # <--- TO JEST NOWY IMPORT

# Importujemy bazę i nasze moduły
from database import engine, Base
from routers import ports, subdomains, directories, history, techstack, dns_scanner

# Tworzy plik bazy danych, jeśli nie istnieje
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recon API", description="Profesjonalne narzędzie OSINT")

# Zarejestrowane moduły (nasze skanery)
app.include_router(ports.router)
app.include_router(subdomains.router)
app.include_router(directories.router)
app.include_router(techstack.router)
app.include_router(dns_scanner.router)
app.include_router(history.router)

# ========================================================
# ZMIANA TUTAJ: Zamiast tekstu, zwracamy plik HTML!
# ========================================================
@app.get("/")
def read_root():
    # Kiedy wejdziesz na http://127.0.0.1:8000/, FastAPI wyśle ten plik:
    return FileResponse("index.html")