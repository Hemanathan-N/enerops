#!/bin/sh

echo "⏳ Waiting for Database connection..."
until python -c "
import asyncio, os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

url = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgrespassword@enerops-db:5432/enerops')
engine = create_async_engine(url)

async def check():
    async with engine.connect() as conn:
        await conn.execute(text('SELECT 1'))

asyncio.run(check())
"; do
  echo "Database is unavailable - sleeping 2 seconds"
  sleep 2
done

echo "🌱 Running Seed Data Script..."
python scripts/seed_data.py

echo "🚀 Starting FastAPI Application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
