import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ScanResult

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/{domain}")
def get_scan_history(domain: str, db: Session = Depends(get_db)):
    records = db.query(ScanResult).filter(ScanResult.domain == domain).all()
    if not records:
        return {"message": "Brak historii dla tej domeny."}

    return {
        "domain": domain,
        "history": [{"id": r.id, "scan_type": r.scan_type, "results": json.loads(r.results_json)} for r in records]
    }