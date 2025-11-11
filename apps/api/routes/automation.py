"""Automation API endpoints for tasks and reminders."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.database import get_db
from apps.api.services.task_automation import TaskAutomationService
from packages.core.models.task import Task
from packages.core.schemas.task import TaskResponse

router = APIRouter()


def orm_to_pydantic(task_orm) -> Task:
    """Convert ORM to Pydantic model."""
    return Task(
        id=task_orm.id,
        lead_id=task_orm.lead_id,
        title=task_orm.title,
        description=task_orm.description,
        task_type=task_orm.task_type,
        status=task_orm.status,
        priority=task_orm.priority,
        assigned_to=task_orm.assigned_to,
        due_date=task_orm.due_date,
        reminder_at=task_orm.reminder_at,
        completed_at=task_orm.completed_at,
        completed_by=task_orm.completed_by,
        created_at=task_orm.created_at,
        updated_at=task_orm.updated_at,
    )


@router.get("/overdue", response_model=List[TaskResponse])
async def get_overdue_tasks(
    db: AsyncSession = Depends(get_db),
):
    """Get all overdue tasks."""
    service = TaskAutomationService(db)
    tasks_orm = await service.get_overdue_tasks()
    return [TaskResponse(**orm_to_pydantic(t).model_dump()) for t in tasks_orm]


@router.get("/reminders", response_model=List[TaskResponse])
async def get_tasks_needing_reminders(
    db: AsyncSession = Depends(get_db),
):
    """Get tasks that need reminders sent."""
    service = TaskAutomationService(db)
    tasks_orm = await service.get_tasks_needing_reminder()
    return [TaskResponse(**orm_to_pydantic(t).model_dump()) for t in tasks_orm]


@router.post("/stale-leads", response_model=List[TaskResponse])
async def create_stale_lead_tasks(
    days_inactive: int = 7,
    db: AsyncSession = Depends(get_db),
):
    """Create follow-up tasks for inactive leads."""
    service = TaskAutomationService(db)
    tasks_orm = await service.auto_create_stale_lead_tasks(days_inactive)
    return [TaskResponse(**orm_to_pydantic(t).model_dump()) for t in tasks_orm]
