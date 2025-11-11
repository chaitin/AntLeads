"""Widget API endpoints."""
import secrets
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.database import get_db
from apps.api.models import WidgetORM, LeadORM
from packages.core.models.lead import LeadSource
from packages.core.schemas.widget import (
    WidgetCreateRequest,
    WidgetUpdateRequest,
    WidgetConfigResponse,
    WidgetFormSubmission,
)
from packages.ml.lead_scoring import auto_tag_lead, score_lead, suggest_lead_priority

router = APIRouter()


def generate_widget_id() -> str:
    """Generate a unique widget ID."""
    return f"wgt_{secrets.token_urlsafe(12)}"


def generate_api_key() -> str:
    """Generate a secure API key."""
    return f"sk_{secrets.token_urlsafe(32)}"


@router.post("/", status_code=201)
async def create_widget(
    request: WidgetCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new widget configuration."""
    widget_orm = WidgetORM(
        name=request.name,
        widget_id=generate_widget_id(),
        api_key=generate_api_key(),
        title=request.title,
        description=request.description,
        submit_button_text=request.submit_button_text,
        success_message=request.success_message,
        fields=request.fields,
        primary_color=request.primary_color,
        button_position=request.button_position,
        auto_open=request.auto_open,
        auto_open_delay=request.auto_open_delay,
    )

    db.add(widget_orm)
    await db.commit()
    await db.refresh(widget_orm)

    return {
        "id": str(widget_orm.id),
        "widget_id": widget_orm.widget_id,
        "api_key": widget_orm.api_key,
        "name": widget_orm.name,
        "embed_code": f'<script src="http://localhost:8000/static/widget.js" data-widget-id="{widget_orm.widget_id}"></script>',
    }


@router.get("/")
async def list_widgets(
    db: AsyncSession = Depends(get_db),
):
    """List all widgets."""
    result = await db.execute(select(WidgetORM))
    widgets = result.scalars().all()

    return {
        "widgets": [
            {
                "id": str(w.id),
                "name": w.name,
                "widget_id": w.widget_id,
                "title": w.title,
                "is_active": w.is_active,
                "created_at": w.created_at.isoformat(),
            }
            for w in widgets
        ]
    }


@router.get("/{widget_id}/config", response_model=WidgetConfigResponse)
async def get_widget_config(
    widget_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get public widget configuration (for embedding)."""
    result = await db.execute(
        select(WidgetORM).where(
            WidgetORM.widget_id == widget_id,
            WidgetORM.is_active == True
        )
    )
    widget = result.scalar_one_or_none()

    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    return WidgetConfigResponse(
        widget_id=widget.widget_id,
        title=widget.title,
        description=widget.description,
        submit_button_text=widget.submit_button_text,
        success_message=widget.success_message,
        fields=widget.fields,
        primary_color=widget.primary_color,
        button_position=widget.button_position,
        auto_open=widget.auto_open,
        auto_open_delay=widget.auto_open_delay,
    )


@router.post("/{widget_id}/submit")
async def submit_widget_form(
    widget_id: str,
    submission: WidgetFormSubmission,
    db: AsyncSession = Depends(get_db),
):
    """Handle form submission from widget."""
    # Verify widget exists and is active
    result = await db.execute(
        select(WidgetORM).where(
            WidgetORM.widget_id == widget_id,
            WidgetORM.is_active == True
        )
    )
    widget = result.scalar_one_or_none()

    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    # Create lead from submission
    from packages.core.models.lead import Lead, ContactInfo

    temp_lead = Lead(
        name=submission.name,
        source=LeadSource.WEB_FORM,
        contact_info=ContactInfo(
            email=submission.email,
            phone=submission.phone,
            company=submission.company,
        ),
        notes=submission.message,
        referrer_url=submission.referrer,
        utm_source="widget",
    )

    # AI scoring and tagging
    score = score_lead(temp_lead)
    suggested_tags = auto_tag_lead(temp_lead)
    suggested_priority = suggest_lead_priority(temp_lead)

    lead_orm = LeadORM(
        name=submission.name,
        source=LeadSource.WEB_FORM,
        score=score,
        priority=suggested_priority,
        contact_info={
            "email": submission.email,
            "phone": submission.phone,
            "company": submission.company,
        },
        tags=suggested_tags,
        notes=submission.message,
        referrer_url=submission.referrer or submission.url,
        utm_source="widget",
        utm_medium=widget_id,
    )

    db.add(lead_orm)
    await db.commit()

    return {
        "success": True,
        "message": widget.success_message,
        "lead_id": str(lead_orm.id),
    }


@router.patch("/{widget_id}")
async def update_widget(
    widget_id: UUID,
    request: WidgetUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Update widget configuration."""
    result = await db.execute(select(WidgetORM).where(WidgetORM.id == widget_id))
    widget = result.scalar_one_or_none()

    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(widget, field, value)

    await db.commit()
    await db.refresh(widget)

    return {
        "id": str(widget.id),
        "widget_id": widget.widget_id,
        "name": widget.name,
    }


@router.delete("/{widget_id}", status_code=204)
async def delete_widget(
    widget_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a widget."""
    result = await db.execute(select(WidgetORM).where(WidgetORM.id == widget_id))
    widget = result.scalar_one_or_none()

    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    await db.delete(widget)
    await db.commit()
