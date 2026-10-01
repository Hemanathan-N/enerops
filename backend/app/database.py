import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Environment variable read pannum; illai enil Docker DB container credentials use pannum
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgrespassword@enerops-db:5432/enerops"
)

engine = create_async_engine(DATABASE_URL, echo=os.getenv("DB_ECHO", "false").lower() == "true")
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
