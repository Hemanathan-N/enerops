from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..database import async_session
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/v1/cost", tags=["Cost"])

async def get_db():
    async with async_session() as session:
        yield session

class CostBreakdown(BaseModel):
    category: str
    amount: float
    color: str

@router.get("/breakdown", response_model=List[CostBreakdown])
async def get_cost_breakdown(db: AsyncSession = Depends(get_db)):
    # Tariff Engine Mock implementation logic for MVP
    # Separate energy readings into peak vs offpeak based on hour for simple demo.
    query = text("""
        SELECT 
            EXTRACT(HOUR FROM time) as hr,
            SUM(kwh)
        FROM energy_readings
        GROUP BY hr
    """)
    result = await db.execute(query)
    rows = result.fetchall()
    
    if not rows:
        return [
            CostBreakdown(category="Peak Usage", amount=1500.50, color="#ef4444"),
            CostBreakdown(category="Off-Peak Usage", amount=890.20, color="#10b981"),
            CostBreakdown(category="Demand Charges", amount=400.00, color="#a855f7")
        ]
        
    peak_kwh = 0
    offpeak_kwh = 0
    
    # Simple logic: 8 AM to 8 PM is Peak, otherwise Off-Peak
    for row in rows:
        hr = int(row[0])
        val = float(row[1])
        if 8 <= hr <= 20:
            peak_kwh += val
        else:
            offpeak_kwh += val
            
    # Assuming Peak rate is $0.20 and Off-Peak logic is $0.10
    peak_cost = peak_kwh * 0.20
    offpeak_cost = offpeak_kwh * 0.10
    
    return [
        CostBreakdown(category="Peak Usage", amount=peak_cost, color="#ef4444"),
        CostBreakdown(category="Off-Peak Usage", amount=offpeak_cost, color="#10b981"),
        CostBreakdown(category="Demand Charges", amount=(peak_kwh/10)*5, color="#a855f7") # Mock demand charge
    ]
