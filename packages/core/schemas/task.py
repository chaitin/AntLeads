"""Task API schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from packages.core.models.task import TaskPriority, TaskStatus, TaskType


class TaskCreateRequest(BaseModel):
    """Request schema for creating a task."""

    lead_id: UUID
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    task_type: TaskType
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: Optional[UUID] = None
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None


class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    task_type: Optional[TaskType] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[UUID] = None
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None


class TaskResponse(BaseModel):
    """Response schema for task data."""

    id: UUID
    lead_id: UUID
    title: str
    description: Optional[str]
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    assigned_to: Optional[UUID]
    due_date: Optional[datetime]
    reminder_at: Optional[datetime]
    completed_at: Optional[datetime]
    completed_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Response schema for paginated task list."""

    tasks: list[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
