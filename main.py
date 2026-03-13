from fastapi import FastAPI
from database import engine, Base
from routers import ports, subdomains, directories, history, techstack, dns_scanner

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recon API", description="Profesjonalne narzędzie OSINT")

# Zarejestrowane moduły
app.include_router(ports.router)
app.include_router(subdomains.router)
app.include_router(directories.router)
app.include_router(techstack.router)      # <--- NOWY
app.include_router(dns_scanner.router)    # <--- NOWY
app.include_router(history.router)

@app.get("/")
def read_root():
    return {"message": "Recon API gotowe do akcji! Wejdź na /docs"}