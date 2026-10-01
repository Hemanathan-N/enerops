from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional
import uuid

from ..database import async_session
from ..models import Plant, Area, ProductionLine, Machine, Meter

router = APIRouter(prefix="/v1/hierarchy", tags=["Hierarchy"])

async def get_db():
    async with async_session() as session:
        yield session

# Pydantic Schemas for response and request
class PlantSchema(BaseModel):
    id: uuid.UUID
    name: str
    location: Optional[str]
    timezone: Optional[str]
    currency: Optional[str]
    class Config:
        from_attributes = True

class AreaSchema(BaseModel):
    id: uuid.UUID
    plant_id: uuid.UUID
    name: str
    area_type: Optional[str]
    class Config:
        from_attributes = True

class ProductionLineSchema(BaseModel):
    id: uuid.UUID
    area_id: uuid.UUID
    name: str
    product_family: Optional[str]
    class Config:
        from_attributes = True

class MachineSchema(BaseModel):
    id: uuid.UUID
    line_id: uuid.UUID
    name: str
    rated_power_kw: Optional[float]
    status: str
    class Config:
        from_attributes = True

# --- Endpoints --- #

@router.get("/plants", response_model=List[PlantSchema])
async def get_plants(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plant))
    return result.scalars().all()

@router.get("/areas", response_model=List[AreaSchema])
async def get_areas(plant_id: Optional[uuid.UUID] = None, db: AsyncSession = Depends(get_db)):
    query = select(Area)
    if plant_id:
        query = query.where(Area.plant_id == plant_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/lines", response_model=List[ProductionLineSchema])
async def get_lines(area_id: Optional[uuid.UUID] = None, db: AsyncSession = Depends(get_db)):
    query = select(ProductionLine)
    if area_id:
        query = query.where(ProductionLine.area_id == area_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/machines", response_model=List[MachineSchema])
async def get_machines(line_id: Optional[uuid.UUID] = None, db: AsyncSession = Depends(get_db)):
    query = select(Machine)
    if line_id:
        query = query.where(Machine.line_id == line_id)
    result = await db.execute(query)
    return result.scalars().all()
