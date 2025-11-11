"""Sample data generator for AntLeads."""
import json
from datetime import datetime, timedelta
from uuid import uuid4

from packages.core.models.lead import LeadPriority, LeadSource, LeadStage
from packages.core.models.task import TaskPriority, TaskStatus, TaskType


def generate_sample_leads():
    """Generate sample lead data."""
    leads = [
        {
            "id": str(uuid4()),
            "name": "John Smith",
            "source": LeadSource.WEB_FORM.value,
            "stage": LeadStage.NEW.value,
            "priority": LeadPriority.HIGH.value,
            "score": 75,
            "contact_info": {
                "email": "john.smith@acme.com",
                "phone": "+1-555-0101",
                "company": "Acme Corporation",
                "title": "Marketing Director",
            },
            "tags": ["enterprise", "hot-lead", "complete-profile"],
            "product_interest": "Enterprise Plan",
            "estimated_value": 50000.0,
            "utm_source": "google",
            "utm_medium": "cpc",
            "utm_campaign": "enterprise-q1",
            "notes": "Interested in demo next week",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": str(uuid4()),
            "name": "Sarah Johnson",
            "source": LeadSource.REFERRAL.value,
            "stage": LeadStage.CONTACTED.value,
            "priority": LeadPriority.URGENT.value,
            "score": 85,
            "contact_info": {
                "email": "sarah.j@techstart.io",
                "phone": "+1-555-0102",
                "company": "TechStart",
                "title": "CEO",
            },
            "tags": ["enterprise", "hot-lead", "high-quality", "complete-profile"],
            "product_interest": "Custom Enterprise Solution",
            "estimated_value": 120000.0,
            "notes": "Referred by current client. Very interested.",
            "created_at": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        },
        {
            "id": str(uuid4()),
            "name": "Mike Chen",
            "source": LeadSource.GOOGLE_ADS.value,
            "stage": LeadStage.QUALIFIED.value,
            "priority": LeadPriority.HIGH.value,
            "score": 68,
            "contact_info": {
                "email": "m.chen@startup.com",
                "phone": "+1-555-0103",
                "company": "Startup Inc",
            },
            "tags": ["mid-market", "warm-lead", "paid-traffic"],
            "product_interest": "Professional Plan",
            "estimated_value": 25000.0,
            "utm_source": "google",
            "utm_medium": "cpc",
            "utm_campaign": "pro-plan-q1",
            "created_at": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        },
        {
            "id": str(uuid4()),
            "name": "Emily Rodriguez",
            "source": LeadSource.EVENT.value,
            "stage": LeadStage.PROPOSAL.value,
            "priority": LeadPriority.URGENT.value,
            "score": 92,
            "contact_info": {
                "email": "emily.r@bigcorp.com",
                "phone": "+1-555-0104",
                "company": "BigCorp Industries",
                "title": "VP of Sales",
            },
            "tags": ["enterprise", "hot-lead", "high-quality", "demo-request"],
            "product_interest": "Enterprise + Custom Integration",
            "estimated_value": 200000.0,
            "notes": "Met at tech conference. Demo completed, waiting for proposal.",
            "created_at": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        },
        {
            "id": str(uuid4()),
            "name": "David Kim",
            "source": LeadSource.LANDING_PAGE.value,
            "stage": LeadStage.NEW.value,
            "priority": LeadPriority.MEDIUM.value,
            "score": 45,
            "contact_info": {
                "email": "david@smallbiz.com",
                "company": "Small Business Solutions",
            },
            "tags": ["smb", "warm-lead"],
            "product_interest": "Basic Plan",
            "estimated_value": 5000.0,
            "created_at": (datetime.utcnow() - timedelta(hours=6)).isoformat(),
        },
    ]

    return leads


def generate_sample_tasks(lead_ids):
    """Generate sample task data."""
    if not lead_ids or len(lead_ids) < 2:
        return []

    tasks = [
        {
            "id": str(uuid4()),
            "lead_id": lead_ids[0],
            "title": "Initial contact call",
            "description": "Call to introduce our services",
            "task_type": TaskType.CALL.value,
            "status": TaskStatus.PENDING.value,
            "priority": TaskPriority.HIGH.value,
            "due_date": (datetime.utcnow() + timedelta(hours=4)).isoformat(),
            "reminder_at": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": str(uuid4()),
            "lead_id": lead_ids[1],
            "title": "Follow up on demo",
            "description": "Check if they have any questions after the demo",
            "task_type": TaskType.FOLLOW_UP.value,
            "status": TaskStatus.PENDING.value,
            "priority": TaskPriority.URGENT.value,
            "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "created_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        },
        {
            "id": str(uuid4()),
            "lead_id": lead_ids[3],
            "title": "Send proposal document",
            "description": "Prepare and send detailed proposal with pricing",
            "task_type": TaskType.PROPOSAL.value,
            "status": TaskStatus.IN_PROGRESS.value,
            "priority": TaskPriority.URGENT.value,
            "due_date": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
            "created_at": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        },
    ]

    return tasks


def save_sample_data():
    """Generate and save sample data to JSON files."""
    leads = generate_sample_leads()
    lead_ids = [lead["id"] for lead in leads]
    tasks = generate_sample_tasks(lead_ids)

    # Save leads
    with open("data/sample/leads.json", "w") as f:
        json.dump(leads, f, indent=2)

    # Save tasks
    with open("data/sample/tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

    print(f"Generated {len(leads)} sample leads")
    print(f"Generated {len(tasks)} sample tasks")
    print("Sample data saved to data/sample/")


if __name__ == "__main__":
    save_sample_data()
