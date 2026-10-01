import asyncio
import os
import random
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import uuid

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models import Base, Plant, Area, ProductionLine, Machine, Meter, Tariff

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://enerops:enerops_password@enerops-db:5432/enerops"
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_hypertables(session: AsyncSession):
    await session.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"))
    await session.execute(text("DROP TABLE IF EXISTS energy_readings CASCADE;"))
    await session.execute(text("DROP TABLE IF EXISTS production_records CASCADE;"))
    await session.execute(text("DROP TABLE IF EXISTS renewable_readings CASCADE;"))

    await session.execute(text("""
    CREATE TABLE IF NOT EXISTS energy_readings (
        time TIMESTAMPTZ NOT NULL,
        meter_id UUID NOT NULL,
        kw DOUBLE PRECISION,
        kwh DOUBLE PRECISION,
        voltage DOUBLE PRECISION,
        current DOUBLE PRECISION,
        power_factor DOUBLE PRECISION,
        quality_status VARCHAR(20)
    );
    """))
    await session.execute(text("SELECT create_hypertable('energy_readings', 'time', if_not_exists => TRUE);"))

    await session.execute(text("""
    CREATE TABLE IF NOT EXISTS production_records (
        time TIMESTAMPTZ NOT NULL,
        line_id UUID NOT NULL,
        product_name VARCHAR(100),
        quantity DOUBLE PRECISION,
        units VARCHAR(20),
        batch_id VARCHAR(50),
        shift_id VARCHAR(50)
    );
    """))
    await session.execute(text("SELECT create_hypertable('production_records', 'time', if_not_exists => TRUE);"))

    await session.execute(text("""
    CREATE TABLE IF NOT EXISTS renewable_readings (
        time TIMESTAMPTZ NOT NULL,
        plant_id UUID NOT NULL,
        source_type VARCHAR(50),
        generation_kwh DOUBLE PRECISION,
        export_kwh DOUBLE PRECISION
    );
    """))
    await session.execute(text("SELECT create_hypertable('renewable_readings', 'time', if_not_exists => TRUE);"))
    await session.commit()

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await create_hypertables(session)
        print("Hypertables created.")

        # Plant
        plant_id = uuid.uuid4()
        plant = Plant(id=plant_id, name="Plant 1 - Manufacturing", location="Detroit, MI", timezone="America/Detroit", currency="USD", peak_contract_limit_mw=5.0)
        session.add(plant)
        await session.flush()

        # Area
        area_id = uuid.uuid4()
        area = Area(id=area_id, plant_id=plant_id, name="Press Shop", area_type="Production")
        session.add(area)
        await session.flush()

        # Line
        line_id = uuid.uuid4()
        line = ProductionLine(id=line_id, area_id=area_id, name="Press Line 03", product_family="Metal Panels")
        session.add(line)
        await session.flush()

        # Machine
        machine_id = uuid.uuid4()
        machine = Machine(id=machine_id, line_id=line_id, name="CNC-104", rated_power_kw=150.0, status="Active")
        session.add(machine)
        await session.flush()

        # Meter
        meter_id = uuid.uuid4()
        meter = Meter(id=meter_id, asset_type="Machine", asset_id=machine_id, source_type="grid", unit="kWh", interval_seconds=900, is_active=True)
        session.add(meter)
        await session.flush()

        await session.commit()
        print("Metadata seeded.")

        # Timeseries Data
        now = datetime.utcnow()
        start_time = now - timedelta(days=30)

        chunk_size = 1000
        buffer = []

        current_time = start_time
        while current_time <= now:
            # Diurnal pattern
            hour = current_time.hour
            is_active_shift = 6 <= hour <= 22
            base_kw = 100.0 if is_active_shift else 15.0
            kw = base_kw + random.uniform(-10, 20)
            kwh = kw * (900.0 / 3600.0) # 15 min intervals

            reading = {
                "time": current_time,
                "meter_id": meter_id,
                "kw": kw,
                "kwh": kwh,
                "voltage": 480.0 + random.uniform(-5, 5),
                "current": (kw * 1000) / (480.0 * 1.732 * 0.9),
                "power_factor": 0.9,
                "quality_status": "OK"
            }
            buffer.append(reading)

            if len(buffer) >= chunk_size:
                await session.execute(text("""
                    INSERT INTO energy_readings (time, meter_id, kw, kwh, voltage, current, power_factor, quality_status)
                    VALUES (:time, :meter_id, :kw, :kwh, :voltage, :current, :power_factor, :quality_status)
                """), buffer)
                buffer = []

            current_time += timedelta(minutes=15)

        if buffer:
             await session.execute(text("""
                 INSERT INTO energy_readings (time, meter_id, kw, kwh, voltage, current, power_factor, quality_status)
                 VALUES (:time, :meter_id, :kw, :kwh, :voltage, :current, :power_factor, :quality_status)
             """), buffer)

        # Seed Production Records
        prod_buffer = []
        prod_time = start_time
        while prod_time <= now:
             prod_buffer.append({
                 "time": prod_time,
                 "line_id": line_id,
                 "product_name": "Metal Panels",
                 "quantity": random.uniform(500, 1500),
                 "units": "units",
                 "batch_id": f"BATCH-{prod_time.strftime('%Y%m%d%H')}",
                 "shift_id": "SHIFT-A"
             })
             if len(prod_buffer) >= chunk_size:
                 await session.execute(text("""
                     INSERT INTO production_records (time, line_id, product_name, quantity, units, batch_id, shift_id)
                     VALUES (:time, :line_id, :product_name, :quantity, :units, :batch_id, :shift_id)
                 """), prod_buffer)
                 prod_buffer = []
             prod_time += timedelta(hours=1)

        if prod_buffer:
             await session.execute(text("""
                 INSERT INTO production_records (time, line_id, product_name, quantity, units, batch_id, shift_id)
                 VALUES (:time, :line_id, :product_name, :quantity, :units, :batch_id, :shift_id)
             """), prod_buffer)

        await session.commit()
        print("Timeseries data seeded.")

if __name__ == "__main__":
    asyncio.run(seed_data())
