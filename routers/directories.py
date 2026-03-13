import httpx
import asyncio
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ScanResult

router = APIRouter(prefix="/scan-directories", tags=["Directories"])
COMMON_PATHS = ["admin", "login", "robots.txt", "backup", "db", ".git", ".env", "api", "config", "test"]

async def check_path(client: httpx.AsyncClient, base_url: str, path: str):
    try:
        response = await client.get(f"{base_url}/{path}", timeout=3.0)
        if response.status_code != 404:
            return {"url": f"{base_url}/{path}", "status": response.status_code}
    except:
        pass
    return None

@router.get("/{domain}")
async def scan_directories(domain: str, db: Session = Depends(get_db)):
    base_url = f"http://{domain}"
    async with httpx.AsyncClient() as client:
        tasks = [check_path(client, base_url, path) for path in COMMON_PATHS]
        results = await asyncio.gather(*tasks)
        found_paths = [res for res in results if res is not None]

    db_record = ScanResult(domain=domain, scan_type="directories", results_json=json.dumps(found_paths))
    db.add(db_record)
    db.commit()

    return {"target": domain, "found_directories": found_paths}