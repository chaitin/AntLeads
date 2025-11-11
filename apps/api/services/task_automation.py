"""Automatic task creation service."""
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models import LeadORM, TaskORM
from packages.core.models.lead import LeadStage
from packages.core.models.task import TaskPriority, TaskStatus, TaskType


class TaskAutomationService:
    """Service for automatic task creation and reminders."""

    def __init__(self, db: AsyncSession):
        """Initialize the service."""
        self.db = db

    async def create_follow_up_task(
        self,
        lead_id: UUID,
        days_from_now: int = 3,
        task_type: TaskType = TaskType.FOLLOW_UP,
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> TaskORM:
        """Create an automatic follow-up task for a lead."""
        # Get lead details
        result = await self.db.execute(select(LeadORM).where(LeadORM.id == lead_id))
        lead = result.scalar_one_or_none()

        if not lead:
            raise ValueError(f"Lead {lead_id} not found")

        due_date = datetime.utcnow() + timedelta(days=days_from_now)
        reminder_at = due_date - timedelta(hours=2)  # Remind 2 hours before

        task = TaskORM(
            lead_id=lead_id,
            title=f"Follow up with {lead.name}",
            description=f"Scheduled follow-up for {lead.stage.value} stage lead",
            task_type=task_type,
            priority=priority,
            assigned_to=lead.assigned_to,
            due_date=due_date,
            reminder_at=reminder_at,
        )

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def create_stage_transition_tasks(
        self,
        lead_id: UUID,
        new_stage: LeadStage,
    ) -> List[TaskORM]:
        """Create tasks based on stage transitions."""
        tasks = []

        # Get lead details
        result = await self.db.execute(select(LeadORM).where(LeadORM.id == lead_id))
        lead = result.scalar_one_or_none()

        if not lead:
            return tasks

        # Stage-specific task creation
        if new_stage == LeadStage.NEW:
            # New lead - create initial contact task
            task = await self._create_task(
                lead_id=lead_id,
                lead_name=lead.name,
                title=f"Initial contact with {lead.name}",
                description="Reach out to new lead within 24 hours",
                task_type=TaskType.CALL,
                priority=TaskPriority.HIGH,
                days_from_now=1,
                assigned_to=lead.assigned_to,
            )
            tasks.append(task)

        elif new_stage == LeadStage.CONTACTED:
            # After contact - schedule follow-up
            task = await self._create_task(
                lead_id=lead_id,
                lead_name=lead.name,
                title=f"Follow up with {lead.name}",
                description="Follow up on initial conversation",
                task_type=TaskType.FOLLOW_UP,
                priority=TaskPriority.MEDIUM,
                days_from_now=3,
                assigned_to=lead.assigned_to,
            )
            tasks.append(task)

        elif new_stage == LeadStage.QUALIFIED:
            # Qualified - schedule demo
            task = await self._create_task(
                lead_id=lead_id,
                lead_name=lead.name,
                title=f"Schedule demo for {lead.name}",
                description="Set up product demonstration",
                task_type=TaskType.DEMO,
                priority=TaskPriority.HIGH,
                days_from_now=2,
                assigned_to=lead.assigned_to,
            )
            tasks.append(task)

        elif new_stage == LeadStage.PROPOSAL:
            # Proposal stage - create proposal task
            task = await self._create_task(
                lead_id=lead_id,
                lead_name=lead.name,
                title=f"Send proposal to {lead.name}",
                description="Prepare and send detailed proposal",
                task_type=TaskType.PROPOSAL,
                priority=TaskPriority.URGENT,
                days_from_now=1,
                assigned_to=lead.assigned_to,
            )
            tasks.append(task)

            # Also create follow-up
            follow_up = await self._create_task(
                lead_id=lead_id,
                lead_name=lead.name,
                title=f"Follow up on proposal with {lead.name}",
                description="Check if they received and reviewed the proposal",
                task_type=TaskType.FOLLOW_UP,
                priority=TaskPriority.HIGH,
                days_from_now=5,
                assigned_to=lead.assigned_to,
            )
            tasks.append(follow_up)

        elif new_stage == LeadStage.NEGOTIATION:
            # Negotiation - schedule meeting
            task = await self._create_task(
                lead_id=lead_id,
                lead_name=lead.name,
                title=f"Negotiation meeting with {lead.name}",
                description="Discuss terms and finalize details",
                task_type=TaskType.MEETING,
                priority=TaskPriority.URGENT,
                days_from_now=2,
                assigned_to=lead.assigned_to,
            )
            tasks.append(task)

        return tasks

    async def _create_task(
        self,
        lead_id: UUID,
        lead_name: str,
        title: str,
        description: str,
        task_type: TaskType,
        priority: TaskPriority,
        days_from_now: int,
        assigned_to: Optional[UUID] = None,
    ) -> TaskORM:
        """Helper to create a task."""
        due_date = datetime.utcnow() + timedelta(days=days_from_now)
        reminder_at = due_date - timedelta(hours=2)

        task = TaskORM(
            lead_id=lead_id,
            title=title,
            description=description,
            task_type=task_type,
            priority=priority,
            assigned_to=assigned_to,
            due_date=due_date,
            reminder_at=reminder_at,
        )

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def get_overdue_tasks(self) -> List[TaskORM]:
        """Get all overdue tasks."""
        query = select(TaskORM).where(
            TaskORM.status == TaskStatus.PENDING,
            TaskORM.due_date < datetime.utcnow(),
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_tasks_needing_reminder(self) -> List[TaskORM]:
        """Get tasks that need reminders sent."""
        query = select(TaskORM).where(
            TaskORM.status == TaskStatus.PENDING,
            TaskORM.reminder_at <= datetime.utcnow(),
            TaskORM.reminder_at.isnot(None),
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def auto_create_stale_lead_tasks(self, days_inactive: int = 7) -> List[TaskORM]:
        """Create tasks for leads that haven't been updated recently."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_inactive)

        query = select(LeadORM).where(
            LeadORM.stage.in_([LeadStage.NEW, LeadStage.CONTACTED, LeadStage.QUALIFIED]),
            LeadORM.updated_at < cutoff_date,
        )

        result = await self.db.execute(query)
        stale_leads = result.scalars().all()

        tasks = []
        for lead in stale_leads:
            # Check if there's already a pending task for this lead
            existing_task_query = select(TaskORM).where(
                TaskORM.lead_id == lead.id,
                TaskORM.status == TaskStatus.PENDING,
            )
            existing_result = await self.db.execute(existing_task_query)
            if existing_result.scalar_one_or_none():
                continue  # Skip if there's already a pending task

            task = await self._create_task(
                lead_id=lead.id,
                lead_name=lead.name,
                title=f"Re-engage with {lead.name}",
                description=f"This lead has been inactive for {days_inactive}+ days. Reach out to re-engage.",
                task_type=TaskType.FOLLOW_UP,
                priority=TaskPriority.MEDIUM,
                days_from_now=1,
                assigned_to=lead.assigned_to,
            )
            tasks.append(task)

        return tasks
