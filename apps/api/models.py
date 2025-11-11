"""SQLAlchemy ORM models."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from apps.api.database import Base
from packages.core.models.lead import LeadPriority, LeadSource, LeadStage
from packages.core.models.task import TaskPriority, TaskStatus, TaskType


class LeadORM(Base):
    """Lead ORM model."""

    __tablename__ = "leads"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False, index=True)
    source = Column(Enum(LeadSource), nullable=False, index=True)
    stage = Column(Enum(LeadStage), nullable=False, default=LeadStage.NEW, index=True)
    priority = Column(Enum(LeadPriority), nullable=False, default=LeadPriority.MEDIUM, index=True)
    score = Column(Integer, default=0, nullable=False)

    # Contact info stored as JSON
    contact_info = Column(JSON, nullable=False, default=dict)
    tags = Column(JSON, nullable=False, default=list)

    # Metadata
    product_interest = Column(String(200), nullable=True)
    estimated_value = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    # Source tracking
    utm_source = Column(String(100), nullable=True, index=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True, index=True)
    referrer_url = Column(String(500), nullable=True)

    # Assignment
    assigned_to = Column(PGUUID(as_uuid=True), nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    contacted_at = Column(DateTime, nullable=True, index=True)
    closed_at = Column(DateTime, nullable=True, index=True)

    # Relationships
    tasks = relationship("TaskORM", back_populates="lead", cascade="all, delete-orphan")


class TaskORM(Base):
    """Task ORM model."""

    __tablename__ = "tasks"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    lead_id = Column(PGUUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(Enum(TaskType), nullable=False, index=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING, index=True)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM, index=True)

    # Assignment
    assigned_to = Column(PGUUID(as_uuid=True), nullable=True, index=True)

    # Scheduling
    due_date = Column(DateTime, nullable=True, index=True)
    reminder_at = Column(DateTime, nullable=True, index=True)

    # Completion
    completed_at = Column(DateTime, nullable=True)
    completed_by = Column(PGUUID(as_uuid=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    lead = relationship("LeadORM", back_populates="tasks")


class LeadTagORM(Base):
    """Lead tag ORM model."""

    __tablename__ = "lead_tags"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True, index=True)
    color = Column(String(7), nullable=False, default="#6B7280")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
