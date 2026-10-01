from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

from ..database import async_session

router = APIRouter(prefix="/v1/ai", tags=["AI"])

async def get_db():
    async with async_session() as session:
        yield session

class ChatRequest(BaseModel):
    message: str

class AnomalyResponse(BaseModel):
    asset_name: str
    time: str
    expected_kwh: float
    actual_kwh: float
    severity: str
    message: str

class ForecastResponse(BaseModel):
    time: str
    predicted_kwh: float

@router.post("/chat")
async def chat_interaction(request: ChatRequest):
    req_lower = request.message.lower()
    if "increase" in req_lower or "yesterday" in req_lower:
        reply = "Based on my analysis, CNC-104 consumed 15% more energy yesterday, which correlates with 2 hours of documented idle time during the off-shift."
    elif "cost" in req_lower:
        reply = "Looking at the cost breakdown, Peak Usage accounts for £1,500 over the past 24 hours. Consider shifting non-critical batch processes to the night shift to save an estimated 10-15%."
    elif "anomaly" in req_lower or "detect" in req_lower:
        reply = "I've detected a critical anomaly on Press Line 03 where consumption exceeded baseline by 40% at 2:00 AM."
    else:
        reply = "I am EnerOps AI. I can help analyze energy trends, investigate anomalies, and simulate cost savings. What aspect of the plant's energy data would you like to investigate?"
    return {"reply": reply}

@router.get("/anomalies", response_model=List[AnomalyResponse])
async def get_anomalies(db: AsyncSession = Depends(get_db)):
    # Mocking anomaly logic: In production we'd use Isolation Forest or statistically compare against `baseline`.
    # MVP: Hardcode an anomaly or inject slight variations.
    return [
        {
            "asset_name": "Press Line 03",
            "time": (datetime.utcnow() - timedelta(hours=5)).strftime("%Y-%m-%d %H:00"),
            "expected_kwh": 350.0,
            "actual_kwh": 485.5,
            "severity": "Critical",
            "message": "Consumption spiked 38% above baseline."
        },
        {
            "asset_name": "CNC-104",
            "time": (datetime.utcnow() - timedelta(hours=14)).strftime("%Y-%m-%d %H:00"),
            "expected_kwh": 120.0,
            "actual_kwh": 145.2,
            "severity": "Warning",
            "message": "Sustained high load during off-peak window."
        }
    ]

@router.get("/forecast", response_model=List[ForecastResponse])
async def get_forecast(db: AsyncSession = Depends(get_db)):
    # A simple pseudo-predictive regression based on next 12 hours.
    # In reality, this would query a serialized scikit-learn model via Pandas.
    ret = []
    base_kwh = 2800.0
    now = datetime.utcnow()
    for i in range(1, 13):
        forecast_time = now + timedelta(hours=i)
        # Sine wave to mock diurnal variation
        offset = random.uniform(-100, 100)
        import math
        diurnal = math.sin((forecast_time.hour / 24.0) * math.pi * 2) * 500
        predicted = max(0, base_kwh + diurnal + offset)
        
        ret.append({
            "time": forecast_time.strftime("%H:00"),
            "predicted_kwh": predicted
        })
    return ret
