"""Task API endpoints."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.database import get_db
from apps.api.models import TaskORM
from packages.core.models.task import Task, TaskStatus
from packages.core.schemas.task import (
    TaskCreateRequest,
    TaskListResponse,
    TaskResponse,
    TaskUpdateRequest,
)

router = APIRouter()


def orm_to_pydantic(task_orm: TaskORM) -> Task:
    """Convert ORM model to Pydantic model."""
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


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    request: TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new task."""
    task_orm = TaskORM(
        lead_id=request.lead_id,
        title=request.title,
        description=request.description,
        task_type=request.task_type,
        priority=request.priority,
        assigned_to=request.assigned_to,
        due_date=request.due_date,
        reminder_at=request.reminder_at,
    )

    db.add(task_orm)
    await db.commit()
    await db.refresh(task_orm)

    task = orm_to_pydantic(task_orm)
    return TaskResponse(**task.model_dump())


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    lead_id: Optional[UUID] = None,
    status: Optional[TaskStatus] = None,
    assigned_to: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    """List tasks with pagination and filtering."""
    query = select(TaskORM)

    # Filters
    if lead_id:
        query = query.where(TaskORM.lead_id == lead_id)
    if status:
        query = query.where(TaskORM.status == status)
    if assigned_to:
        query = query.where(TaskORM.assigned_to == assigned_to)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Paginate
    query = query.order_by(TaskORM.due_date.asc().nullslast(), TaskORM.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    tasks_orm = result.scalars().all()

    tasks = [TaskResponse(**orm_to_pydantic(task).model_dump()) for task in tasks_orm]

    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific task by ID."""
    result = await db.execute(select(TaskORM).where(TaskORM.id == task_id))
    task_orm = result.scalar_one_or_none()

    if not task_orm:
        raise HTTPException(status_code=404, detail="Task not found")

    task = orm_to_pydantic(task_orm)
    return TaskResponse(**task.model_dump())


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    request: TaskUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Update a task."""
    result = await db.execute(select(TaskORM).where(TaskORM.id == task_id))
    task_orm = result.scalar_one_or_none()

    if not task_orm:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task_orm, field, value)

    # Track completion
    if request.status and request.status == TaskStatus.COMPLETED and not task_orm.completed_at:
        task_orm.completed_at = datetime.utcnow()
        # Note: In a real app, you'd get the current user ID from auth
        # task_orm.completed_by = current_user.id

    task_orm.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task_orm)

    task = orm_to_pydantic(task_orm)
    return TaskResponse(**task.model_dump())


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a task."""
    result = await db.execute(select(TaskORM).where(TaskORM.id == task_id))
    task_orm = result.scalar_one_or_none()

    if not task_orm:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task_orm)
    await db.commit()
