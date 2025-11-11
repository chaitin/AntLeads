"""Import sample data into the database."""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.database import AsyncSessionLocal, init_db
from apps.api.models import LeadORM, TaskORM
from packages.core.models.lead import LeadPriority, LeadSource, LeadStage
from packages.core.models.task import TaskPriority, TaskStatus, TaskType


async def import_leads(session: AsyncSession):
    """Import leads from JSON file."""
    json_path = Path("data/sample/leads.json")

    if not json_path.exists():
        print(f"Leads file not found: {json_path}")
        return

    with open(json_path, "r") as f:
        leads_data = json.load(f)

    print(f"Importing {len(leads_data)} leads...")

    for lead_data in leads_data:
        lead = LeadORM(
            id=UUID(lead_data["id"]),
            name=lead_data["name"],
            source=LeadSource(lead_data["source"]),
            stage=LeadStage(lead_data["stage"]),
            priority=LeadPriority(lead_data["priority"]),
            score=lead_data["score"],
            contact_info=lead_data["contact_info"],
            tags=lead_data["tags"],
            product_interest=lead_data.get("product_interest"),
            estimated_value=lead_data.get("estimated_value"),
            notes=lead_data.get("notes"),
            utm_source=lead_data.get("utm_source"),
            utm_medium=lead_data.get("utm_medium"),
            utm_campaign=lead_data.get("utm_campaign"),
            referrer_url=lead_data.get("referrer_url"),
            created_at=datetime.fromisoformat(lead_data["created_at"]),
        )
        session.add(lead)

    await session.commit()
    print(f"✓ Imported {len(leads_data)} leads")


async def import_tasks(session: AsyncSession):
    """Import tasks from JSON file."""
    json_path = Path("data/sample/tasks.json")

    if not json_path.exists():
        print(f"Tasks file not found: {json_path}")
        return

    with open(json_path, "r") as f:
        tasks_data = json.load(f)

    print(f"Importing {len(tasks_data)} tasks...")

    for task_data in tasks_data:
        task = TaskORM(
            id=UUID(task_data["id"]),
            lead_id=UUID(task_data["lead_id"]),
            title=task_data["title"],
            description=task_data.get("description"),
            task_type=TaskType(task_data["task_type"]),
            status=TaskStatus(task_data["status"]),
            priority=TaskPriority(task_data["priority"]),
            due_date=datetime.fromisoformat(task_data["due_date"]) if task_data.get("due_date") else None,
            reminder_at=datetime.fromisoformat(task_data["reminder_at"]) if task_data.get("reminder_at") else None,
            created_at=datetime.fromisoformat(task_data["created_at"]),
        )
        session.add(task)

    await session.commit()
    print(f"✓ Imported {len(tasks_data)} tasks")


async def main():
    """Main import function."""
    print("Initializing database...")
    await init_db()

    async with AsyncSessionLocal() as session:
        try:
            await import_leads(session)
            await import_tasks(session)
            print("\n✓ Sample data imported successfully!")
        except Exception as e:
            print(f"\n✗ Error importing data: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
