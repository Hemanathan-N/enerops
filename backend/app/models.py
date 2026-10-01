from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .database import Base
import uuid
import datetime

class Plant(Base):
    __tablename__ = "plants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    location = Column(String)
    timezone = Column(String)
    currency = Column(String)
    peak_contract_limit_mw = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Area(Base):
    __tablename__ = "areas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"))
    name = Column(String)
    area_type = Column(String)

class ProductionLine(Base):
    __tablename__ = "production_lines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id"))
    name = Column(String)
    product_family = Column(String)

class Machine(Base):
    __tablename__ = "machines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line_id = Column(UUID(as_uuid=True), ForeignKey("production_lines.id"))
    name = Column(String)
    rated_power_kw = Column(Float)
    status = Column(String)

class Meter(Base):
    __tablename__ = "meters"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_type = Column(String)
    asset_id = Column(UUID(as_uuid=True))
    source_type = Column(String)
    unit = Column(String)
    interval_seconds = Column(Integer)
    is_active = Column(Boolean, default=True)

class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"))
    name = Column(String)
    effective_from = Column(DateTime)
    effective_to = Column(DateTime)
    time_bands = Column(JSONB)
    peak_rate = Column(Float)
    off_peak_rate = Column(Float)
    demand_charge_per_kw = Column(Float)
    fixed_charge = Column(Float)

class Baseline(Base):
    __tablename__ = "baselines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_type = Column(String)
    asset_id = Column(UUID(as_uuid=True))
    model_version = Column(String)
    expected_kwh_per_unit = Column(Float)
    dynamic_formula = Column(JSONB)

class Anomaly(Base):
    __tablename__ = "anomalies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_type = Column(String)
    asset_id = Column(UUID(as_uuid=True))
    detected_at = Column(DateTime)
    severity = Column(String)  # Critical, Warning, Info
    score = Column(Float)
    expected_kwh = Column(Float)
    actual_kwh = Column(Float)
    explanation = Column(String)
    status = Column(String)

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"))
    asset_id = Column(UUID(as_uuid=True))
    recommendation = Column(String)
    estimated_saving_currency = Column(Float)
    estimated_kwh_saving = Column(Float)
    estimated_co2_saving = Column(Float)
    confidence = Column(Float)
    owner = Column(String)
    status = Column(String)  # Open, In-Progress, Realized

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"))
    alert_type = Column(String)
    severity = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
