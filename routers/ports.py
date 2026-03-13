import asyncio
import socket
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ScanResult

router = APIRouter(prefix="/scan-ports", tags=["Ports"])
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 8080]

async def check_port(ip: str, port: int):
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        writer.close()
        await writer.wait_closed()
        return {"port": port, "status": "open"}
    except:
        return {"port": port, "status": "closed"}

@router.get("/{domain}")
async def scan_domain_ports(domain: str, db: Session = Depends(get_db)):
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return {"error": "Nie można rozwiązać nazwy domeny."}

    tasks = [check_port(ip, port) for port in COMMON_PORTS]
    results = await asyncio.gather(*tasks)
    open_ports = [res["port"] for res in results if res.get("status") == "open"]

    db_record = ScanResult(domain=domain, scan_type="ports", results_json=json.dumps(open_ports))
    db.add(db_record)
    db.commit()

    return {"target": domain, "ip": ip, "open_ports": open_ports, "status": "Zapisano!"}