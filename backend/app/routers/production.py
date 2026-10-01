from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..database import async_session
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/v1/production", tags=["Production"])

async def get_db():
    async with async_session() as session:
        yield session

class ProductionTimeseries(BaseModel):
    time: str
    units: float

class EnergyIntensity(BaseModel):
    name: str
    intensity: float

@router.get("/timeseries", response_model=List[ProductionTimeseries])
async def get_production_timeseries(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT 
            time_bucket('1 hour', time) AS bucket,
            SUM(quantity) as total_units
        FROM production_records
        GROUP BY bucket
        ORDER BY bucket DESC
        LIMIT 24
    """)
    result = await db.execute(query)
    rows = result.fetchall()
    
    if not rows:
        # Mock fallback
        import random
        return [ProductionTimeseries(time=f"{i}:00", units=random.uniform(500, 1500)) for i in range(24)]
    
    ret = []
    for row in reversed(rows):
        ret.append({
            "time": row[0].strftime("%H:%00"),
            "units": float(row[1])
        })
    return ret

@router.get("/intensity", response_model=List[EnergyIntensity])
async def get_intensity(db: AsyncSession = Depends(get_db)):
    # To join production records and energy readings, they need to be grouped by line and time
    # This MVP simplifies it by mocking intensity per area based on db structure
    query = text("""
        SELECT a.name, SUM(er.kwh), 3000 as mock_units 
        FROM areas a
        JOIN production_lines pl ON pl.area_id = a.id
        JOIN machines m ON m.line_id = pl.id
        JOIN meters me ON me.asset_id = m.id
        JOIN energy_readings er ON er.meter_id = me.id
        GROUP BY a.name
    """)
    result = await db.execute(query)
    rows = result.fetchall()
    
    ret = []
    for row in rows:
        kwh = float(row[1])
        units = float(row[2])
        ret.append({
            "name": row[0],
            "intensity": kwh / units if units > 0 else 0
        })
    return ret
