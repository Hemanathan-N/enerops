from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..database import async_session
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter(prefix="/v1/energy", tags=["Energy"])

async def get_db():
    async with async_session() as session:
        yield session

class TimeseriesData(BaseModel):
    time: str
    kwh: float
    baseline: float

class DistributionData(BaseModel):
    name: str
    value: float
    color: str

@router.get("/metrics")
async def get_metrics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT SUM(kwh) FROM energy_readings"))
    total_energy = result.scalar() or 0.0
    
    # Simple hardcoded cost logic for MVP
    cost = total_energy * 0.15
    
    return {
        "total_energy_consumption_kwh": total_energy,
        "energy_cost_currency": cost,
        "production_output_units": 38420,
        "energy_intensity_kwh_per_unit": total_energy / 38420 if total_energy > 0 else 0,
        "co2_emissions_tco2e": total_energy * 0.0004,
        "renewable_contribution_pct": 38.4
    }

@router.get("/timeseries", response_model=List[TimeseriesData])
async def get_timeseries(db: AsyncSession = Depends(get_db)):
    # Group by day or 15-minute interval? We'll group by latest 24 hours.
    # For MVP we will just return 24 hours of data.
    # In SQLite or Postgres, we use time_bucket for TSDB, but fallback to date_trunc.
    # Given we have timescaledb:
    query = text("""
        SELECT 
            time_bucket('1 hour', time) AS bucket,
            SUM(kwh) as total_kwh
        FROM energy_readings
        GROUP BY bucket
        ORDER BY bucket DESC
        LIMIT 24
    """)
    result = await db.execute(query)
    rows = result.fetchall()
    
    # Fallback to random if no rows
    if not rows:
        import random
        return [TimeseriesData(time=f"{i}:00", kwh=random.uniform(2000, 5000), baseline=3000) for i in range(24)]
    
    # Format and reverse
    ret = []
    # Reverse to have oldest first
    for row in reversed(rows):
        # bucket is datetime
        ret.append({
            "time": row[0].strftime("%H:%00"),
            "kwh": float(row[1]),
            "baseline": float(row[1]) * 0.95 # Mock baseline
        })
    return ret

@router.get("/distribution", response_model=List[DistributionData])
async def get_distribution(db: AsyncSession = Depends(get_db)):
    # Get total energy by area
    # `energy_readings` has meter_id
    # `meters` has asset_id (machine)
    # `machines` has line_id
    # `production_lines` has area_id
    # `areas` has name
    
    query = text("""
        SELECT a.name, SUM(er.kwh)
        FROM areas a
        JOIN production_lines pl ON pl.area_id = a.id
        JOIN machines m ON m.line_id = pl.id
        JOIN meters me ON me.asset_id = m.id
        JOIN energy_readings er ON er.meter_id = me.id
        GROUP BY a.name
    """)
    result = await db.execute(query)
    rows = result.fetchall()
    
    colors = ["#3b82f6", "#ef4444", "#f97316", "#a855f7", "#06b6d4", "#8b5cf6"]
    
    ret = []
    for i, row in enumerate(rows):
        ret.append({
            "name": row[0],
            "value": float(row[1]),
            "color": colors[i % len(colors)]
        })
        
    return ret
