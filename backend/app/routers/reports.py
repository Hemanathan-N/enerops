from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..database import async_session
from ..auth import get_current_user

router = APIRouter(prefix="/v1/reports", tags=["Reports"])

async def get_db():
    async with async_session() as session:
        yield session

class DailyReport(BaseModel):
    date: str
    total_energy_kwh: float
    total_cost: float
    production_units: float
    anomalies_count: int
    top_consumers: List[dict]

@router.get("/daily", response_model=DailyReport)
async def get_daily_report(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not permitted to generate management reports. Requires 'manager' or 'admin' role.")

    # In production, this synthesizes multiple complex subqueries
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Using simplistic mocks consistent with earlier MVP
    return DailyReport(
        date=date_str,
        total_energy_kwh=128450,
        total_cost=982000,
        production_units=38420,
        anomalies_count=2,
        top_consumers=[
            {"asset": "Press Line 03", "kwh": 35400, "pct": 28},
            {"asset": "Welding Shop", "kwh": 22350, "pct": 18}
        ]
    )
