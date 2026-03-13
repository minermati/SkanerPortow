import httpx
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ScanResult

router = APIRouter(prefix="/scan-subdomains", tags=["Subdomains"])


@router.get("/{domain}")
async def get_subdomains(domain: str, db: Session = Depends(get_db)):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=15.0)
            if response.status_code != 200:
                return {"error": "Baza certyfikatów niedostępna."}

            data = response.json()
            subdomains = {entry['name_value'].lower().split("\n")[0] for entry in data}
            final_subdomains = sorted(list(subdomains))

            db_record = ScanResult(domain=domain, scan_type="subdomains", results_json=json.dumps(final_subdomains))
            db.add(db_record)
            db.commit()

            return {"target": domain, "count": len(final_subdomains), "subdomains": final_subdomains}
        except Exception as e:
            return {"error": f"Błąd: {str(e)}"}