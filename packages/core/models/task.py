"""Task-related business models."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel


class TaskType(str, Enum):
    """Task type enumeration."""

    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    FOLLOW_UP = "follow_up"
    PROPOSAL = "proposal"
    DEMO = "demo"
    NOTE = "note"
    OTHER = "other"


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class TaskPriority(str, Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(BaseModel):
    """Task business model."""

    id: Optional[UUID] = None
    lead_id: UUID
    title: str
    description: Optional[str] = None
    task_type: TaskType
    status: Optional[TaskStatus] = TaskStatus.PENDING
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM

    # Assignment
    assigned_to: Optional[UUID] = None

    # Scheduling
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None

    # Completion
    completed_at: Optional[datetime] = None
    completed_by: Optional[UUID] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None