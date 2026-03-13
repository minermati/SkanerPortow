import httpx
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ScanResult

router = APIRouter(prefix="/scan-tech", tags=["Tech Stack"])


@router.get("/{domain}")
async def scan_tech_stack(domain: str, db: Session = Depends(get_db)):
    url = f"http://{domain}"
    tech_info = {}

    async with httpx.AsyncClient() as client:
        try:
            # Używamy prostego zapytania HEAD, bo interesują nas tylko nagłówki
            response = await client.head(url, timeout=5.0, follow_redirects=True)
            headers = response.headers

            # Analizujemy nagłówki w poszukiwaniu technologii
            if "Server" in headers:
                tech_info["Serwer"] = headers["Server"]
            if "X-Powered-By" in headers:
                tech_info["Technologia"] = headers["X-Powered-By"]
            if "X-AspNet-Version" in headers:
                tech_info["ASP.NET"] = headers["X-AspNet-Version"]

            # Zabezpieczenia (Security Headers)
            tech_info["Zabezpieczenia"] = {
                "Strict-Transport-Security": "HSTS" in headers,
                "X-Frame-Options": "X-Frame-Options" in headers,
                "X-XSS-Protection": "X-XSS-Protection" in headers
            }

            # Zapis do bazy
            db_record = ScanResult(domain=domain, scan_type="tech_stack", results_json=json.dumps(tech_info))
            db.add(db_record)
            db.commit()

            return {"target": domain, "tech_stack": tech_info}

        except Exception as e:
            return {"error": f"Nie udało się pobrać nagłówków: {str(e)}"}