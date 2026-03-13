from sqlalchemy import Column, Integer, String, Text
from database import Base

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)
    scan_type = Column(String)
    results_json = Column(Text)