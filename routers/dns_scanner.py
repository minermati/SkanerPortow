import json
import dns.asyncresolver
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ScanResult

router = APIRouter(prefix="/scan-dns", tags=["DNS Records"])

async def get_records(domain: str, record_type: str):
    try:
        answers = await dns.asyncresolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except Exception:
        return []

@router.get("/{domain}")
async def scan_dns_records(domain: str, db: Session = Depends(get_db)):
    # Zbieramy różne typy rekordów
    results = {
        "A (Adresy IP)": await get_records(domain, "A"),
        "MX (Serwery Poczty)": await get_records(domain, "MX"),
        "NS (Serwery Nazw)": await get_records(domain, "NS"),
        "TXT (Notatki / SPF)": await get_records(domain, "TXT"),
    }

    # Zapis do bazy
    db_record = ScanResult(domain=domain, scan_type="dns", results_json=json.dumps(results))
    db.add(db_record)
    db.commit()

    return {"target": domain, "dns_records": results}