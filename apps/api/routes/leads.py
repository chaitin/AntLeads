"""Lead API endpoints."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.database import get_db
from apps.api.models import LeadORM
from packages.core.models.lead import ContactInfo, Lead, LeadStage
from packages.core.schemas.lead import (
    LeadCreateRequest,
    LeadImportRequest,
    LeadImportResponse,
    LeadListResponse,
    LeadResponse,
    LeadStatsResponse,
    LeadUpdateRequest,
)
from packages.ml.lead_scoring import auto_tag_lead, score_lead, suggest_lead_priority
from apps.api.services.task_automation import TaskAutomationService

router = APIRouter()


def orm_to_pydantic(lead_orm: LeadORM) -> Lead:
    """Convert ORM model to Pydantic model."""
    return Lead(
        id=lead_orm.id,
        name=lead_orm.name,
        source=lead_orm.source,
        stage=lead_orm.stage,
        priority=lead_orm.priority,
        score=lead_orm.score,
        contact_info=ContactInfo(**lead_orm.contact_info) if lead_orm.contact_info else ContactInfo(),
        tags=lead_orm.tags or [],
        product_interest=lead_orm.product_interest,
        estimated_value=lead_orm.estimated_value,
        notes=lead_orm.notes,
        utm_source=lead_orm.utm_source,
        utm_medium=lead_orm.utm_medium,
        utm_campaign=lead_orm.utm_campaign,
        referrer_url=lead_orm.referrer_url,
        assigned_to=lead_orm.assigned_to,
        created_at=lead_orm.created_at,
        updated_at=lead_orm.updated_at,
        contacted_at=lead_orm.contacted_at,
        closed_at=lead_orm.closed_at,
    )


@router.post("/", response_model=LeadResponse, status_code=201)
async def create_lead(
    request: LeadCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new lead with AI scoring and auto-tagging."""
    # Create initial lead for scoring
    temp_lead = Lead(
        name=request.name,
        source=request.source,
        contact_info=request.contact_info,
        tags=request.tags,
        product_interest=request.product_interest,
        estimated_value=request.estimated_value,
        notes=request.notes,
        utm_source=request.utm_source,
        utm_medium=request.utm_medium,
        utm_campaign=request.utm_campaign,
        referrer_url=request.referrer_url,
    )

    # AI scoring and tagging
    score = score_lead(temp_lead)
    suggested_tags = auto_tag_lead(temp_lead)
    suggested_priority = suggest_lead_priority(temp_lead)

    # Merge user tags with AI suggested tags
    all_tags = list(set(request.tags + suggested_tags))

    lead_orm = LeadORM(
        name=request.name,
        source=request.source,
        score=score,
        priority=suggested_priority,
        contact_info=request.contact_info.model_dump(),
        tags=all_tags,
        product_interest=request.product_interest,
        estimated_value=request.estimated_value,
        notes=request.notes,
        utm_source=request.utm_source,
        utm_medium=request.utm_medium,
        utm_campaign=request.utm_campaign,
        referrer_url=request.referrer_url,
    )

    db.add(lead_orm)
    await db.commit()
    await db.refresh(lead_orm)

    lead = orm_to_pydantic(lead_orm)
    return LeadResponse(**lead.model_dump())


@router.get("/", response_model=LeadListResponse)
async def list_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    stage: Optional[LeadStage] = None,
    source: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List leads with pagination and filtering."""
    query = select(LeadORM)

    # Filters
    if stage:
        query = query.where(LeadORM.stage == stage)
    if source:
        query = query.where(LeadORM.source == source)
    if search:
        query = query.where(
            (LeadORM.name.ilike(f"%{search}%"))
            | (LeadORM.contact_info["email"].as_string().ilike(f"%{search}%"))
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Paginate
    query = query.order_by(LeadORM.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    leads_orm = result.scalars().all()

    leads = [LeadResponse(**orm_to_pydantic(lead).model_dump()) for lead in leads_orm]

    return LeadListResponse(
        leads=leads,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific lead by ID."""
    result = await db.execute(select(LeadORM).where(LeadORM.id == lead_id))
    lead_orm = result.scalar_one_or_none()

    if not lead_orm:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead = orm_to_pydantic(lead_orm)
    return LeadResponse(**lead.model_dump())


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: UUID,
    request: LeadUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Update a lead and auto-create tasks on stage transitions."""
    result = await db.execute(select(LeadORM).where(LeadORM.id == lead_id))
    lead_orm = result.scalar_one_or_none()

    if not lead_orm:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Track old stage for automation
    old_stage = lead_orm.stage

    # Update fields
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "contact_info" and value is not None:
            setattr(lead_orm, field, value.model_dump())
        else:
            setattr(lead_orm, field, value)

    # Track contacted_at
    if request.stage and request.stage == LeadStage.CONTACTED and not lead_orm.contacted_at:
        lead_orm.contacted_at = datetime.utcnow()

    # Track closed_at
    if request.stage and request.stage in [LeadStage.WON, LeadStage.LOST] and not lead_orm.closed_at:
        lead_orm.closed_at = datetime.utcnow()

    lead_orm.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(lead_orm)

    # Auto-create tasks on stage change
    if request.stage and request.stage != old_stage:
        task_service = TaskAutomationService(db)
        await task_service.create_stage_transition_tasks(lead_id, request.stage)

    lead = orm_to_pydantic(lead_orm)
    return LeadResponse(**lead.model_dump())


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a lead."""
    result = await db.execute(select(LeadORM).where(LeadORM.id == lead_id))
    lead_orm = result.scalar_one_or_none()

    if not lead_orm:
        raise HTTPException(status_code=404, detail="Lead not found")

    await db.delete(lead_orm)
    await db.commit()


@router.post("/import", response_model=LeadImportResponse)
async def import_leads(
    request: LeadImportRequest,
    db: AsyncSession = Depends(get_db),
):
    """Bulk import leads."""
    successful = 0
    failed = 0
    errors = []

    for idx, lead_data in enumerate(request.leads):
        try:
            lead_orm = LeadORM(
                name=lead_data.name,
                source=request.source,
                contact_info=lead_data.contact_info.model_dump(),
                tags=lead_data.tags,
                product_interest=lead_data.product_interest,
                estimated_value=lead_data.estimated_value,
                notes=lead_data.notes,
                utm_source=lead_data.utm_source,
                utm_medium=lead_data.utm_medium,
                utm_campaign=lead_data.utm_campaign,
                referrer_url=lead_data.referrer_url,
            )
            db.add(lead_orm)
            successful += 1
        except Exception as e:
            failed += 1
            errors.append({
                "index": idx,
                "name": lead_data.name,
                "error": str(e),
            })

    await db.commit()

    return LeadImportResponse(
        total=len(request.leads),
        successful=successful,
        failed=failed,
        errors=errors,
    )


@router.get("/stats/overview", response_model=LeadStatsResponse)
async def get_lead_stats(
    db: AsyncSession = Depends(get_db),
):
    """Get lead statistics overview."""
    # Total leads
    result = await db.execute(select(func.count(LeadORM.id)))
    total_leads = result.scalar_one()

    # By stage
    result = await db.execute(
        select(LeadORM.stage, func.count(LeadORM.id))
        .group_by(LeadORM.stage)
    )
    by_stage = {str(stage): count for stage, count in result.all()}

    # By source
    result = await db.execute(
        select(LeadORM.source, func.count(LeadORM.id))
        .group_by(LeadORM.source)
    )
    by_source = {str(source): count for source, count in result.all()}

    # By priority
    result = await db.execute(
        select(LeadORM.priority, func.count(LeadORM.id))
        .group_by(LeadORM.priority)
    )
    by_priority = {str(priority): count for priority, count in result.all()}

    # Average score
    result = await db.execute(select(func.avg(LeadORM.score)))
    average_score = result.scalar_one() or 0.0

    # Total estimated value
    result = await db.execute(
        select(func.sum(LeadORM.estimated_value))
        .where(LeadORM.estimated_value.isnot(None))
    )
    total_estimated_value = result.scalar_one() or 0.0

    return LeadStatsResponse(
        total_leads=total_leads,
        by_stage=by_stage,
        by_source=by_source,
        by_priority=by_priority,
        average_score=float(average_score),
        total_estimated_value=float(total_estimated_value),
    )
